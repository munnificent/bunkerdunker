# utils/achievement_utils.py

import logging
from typing import List
from sqlalchemy.orm import Session
from telebot import TeleBot

from models import Player, Achievement, PlayerAchievement

# --- Конфигурация достижений ---
# Централизованный список всех достижений и условий их получения.
# Чтобы добавить новое достижение, просто добавьте сюда новый словарь.
ACHIEVEMENT_CONDITIONS = [
    {
        "name": "Первая победа",
        "description": "Победите в игре впервые.",
        "condition": lambda p: p.wins == 1,
        "icon": "🏅"
    },
    {
        "name": "Ветеран Бункера",
        "description": "Примите участие в 5 играх.",
        "condition": lambda p: (p.wins + p.losses) >= 5,
        "icon": "🎖️"
    },
    {
        "name": "Легенда Бункера",
        "description": "Победите в 10 играх.",
        "condition": lambda p: p.wins >= 10,
        "icon": "🏆"
    },
    # --- Место для новых достижений ---
    # {
    #     "name": "Непобедимый",
    #     "description": "Выиграйте 3 игры подряд (потребует доработки модели Player).",
    #     "condition": lambda p: p.win_streak == 3,
    #     "icon": "🔥"
    # },
]

def award_new_achievements(bot: TeleBot, player: Player, session: Session) -> None:
    """
    Проверяет и присваивает игроку новые достижения, а затем отправляет уведомления.

    Args:
        bot: Экземпляр бота для отправки сообщений.
        player: Объект игрока для проверки.
        session: Активная сессия SQLAlchemy.
    """
    try:
        newly_awarded = _check_player_achievements(player, session)

        if not newly_awarded:
            return

        # Сохраняем все новые достижения в базе данных одной транзакцией
        session.add_all(newly_awarded)
        session.commit()
        logging.info(f"Игроку {player.username} ({player.id}) присвоены новые достижения: {[ach.achievement.name for ach in newly_awarded]}.")

        # Отправляем уведомления игроку
        for player_achievement in newly_awarded:
            achievement = player_achievement.achievement
            icon = next((item['icon'] for item in ACHIEVEMENT_CONDITIONS if item['name'] == achievement.name), '✨')
            message = f"{icon} Вы получили достижение: <b>{achievement.name}</b>!\n<i>{achievement.description}</i>"
            bot.send_message(player.telegram_id, message, parse_mode='HTML')

    except Exception as e:
        logging.error(f"Ошибка при проверке или присвоении достижений для игрока {player.id}: {e}", exc_info=True)
        session.rollback()


def _check_player_achievements(player: Player, session: Session) -> List[PlayerAchievement]:
    """
    Проверяет условия и возвращает список новых, еще не присвоенных достижений.
    Не сохраняет изменения в БД, только формирует объекты.
    
    Args:
        player: Объект игрока для проверки.
        session: Активная сессия SQLAlchemy.

    Returns:
        Список новых объектов PlayerAchievement, готовых к добавлению в сессию.
    """
    # 1. Получаем все существующие ID достижений игрока одним запросом
    player_achievement_ids = {
        ach.achievement_id for ach in player.achievements
    }

    # 2. Получаем все возможные достижения из базы данных одним запросом
    all_achievements = {ach.name: ach for ach in session.query(Achievement).all()}
    
    newly_awarded = []

    # 3. Проверяем условия в коде, минимизируя запросы к БД
    for config in ACHIEVEMENT_CONDITIONS:
        achievement_name = config["name"]
        
        # Пропускаем, если такого достижения нет в БД
        if achievement_name not in all_achievements:
            logging.warning(f"Достижение '{achievement_name}' настроено, но не найдено в базе данных.")
            continue
            
        achievement = all_achievements[achievement_name]

        # Проверяем, есть ли у игрока уже это достижение и выполнено ли условие
        if achievement.id not in player_achievement_ids and config["condition"](player):
            new_player_achievement = PlayerAchievement(
                player_id=player.id,
                achievement_id=achievement.id
            )
            newly_awarded.append(new_player_achievement)
            # Добавляем ID в сет, чтобы не выдать достижение дважды в одной сессии
            player_achievement_ids.add(achievement.id)

    return newly_awarded