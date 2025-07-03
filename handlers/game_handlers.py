# handlers/game_handlers.py

import logging
from functools import wraps
from typing import List

from sqlalchemy.orm import Session, joinedload
from telebot import TeleBot
from telebot.types import Message, APIError

# Импортируем декораторы из других модулей, чтобы не дублировать код
from handlers.create_room_handler import player_required
from handlers.chat_handlers import player_in_room_required, _broadcast_to_room
from models import Player, Room, Characteristic, PlayerAchievement


# --- Вспомогательные функции ---

def _get_player_characteristics_text(player: Player) -> str:
    """Формирует и возвращает текст с характеристиками игрока."""
    characteristics = player.characteristics
    if not characteristics:
        return "❗ У вас пока нет характеристик. Их выдадут в начале игры."

    return (
        f"<b>Ваши текущие характеристики:</b>\n\n"
        f"👤 <b>Профессия:</b> {characteristics.profession}\n"
        f"🧬 <b>Биология:</b> {characteristics.biology}\n"
        f"❤️ <b>Здоровье:</b> {characteristics.health}\n"
        f"🎨 <b>Хобби:</b> {characteristics.hobby}\n"
        f"🎒 <b>Багаж:</b> {characteristics.luggage}\n"
        f"📜 <b>Факт:</b> {characteristics.facts}\n"
        f"😱 <b>Фобия:</b> {characteristics.phobia}\n"
        f"✨ <b>Талант:</b> {characteristics.talent}\n"
        f"🏷️ <b>Социальный статус:</b> {characteristics.social_status}"
    )

def _get_achievements_text(player_achievements: List[PlayerAchievement]) -> str:
    """Формирует и возвращает текст со списком достижений игрока."""
    if not player_achievements:
        return "🎖️ У вас пока нет достижений. Первая победа уже близко!"

    achievement_lines = []
    # Сортируем по дате получения
    for pa in sorted(player_achievements, key=lambda x: x.date_achieved):
        # Используем данные из уже загруженного объекта Achievement
        achievement = pa.achievement
        achievement_lines.append(f"🏅 <b>{achievement.name}</b>: <i>{achievement.description}</i>")
    
    return "<b>Ваши достижения:</b>\n\n" + "\n\n".join(achievement_lines)


# --- Обработчики команд ---

@player_in_room_required
def handle_show_status(bot: TeleBot, message: Message, session: Session, player: Player, room: Room):
    """
    Обрабатывает команду /show_status.
    Показывает игроку его текущие игровые характеристики.
    """
    logging.info(f"Игрок {player.username} запросил свои характеристики в комнате {room.code}.")
    
    char_text = _get_player_characteristics_text(player)
    bot.send_message(player.telegram_id, char_text, parse_mode='HTML')


@player_in_room_required
def handle_leave_room(bot: TeleBot, message: Message, session: Session, player: Player, room: Room):
    """
    Обрабатывает команду /leave_room.
    Позволяет игроку покинуть текущую комнату.
    """
    logging.info(f"Игрок {player.username} покидает комнату {room.code}.")

    # Уведомляем остальных игроков
    notification_text = f"👤 Игрок <b>{player.username}</b> покинул комнату."
    
    # Создаем копию списка, так как игрок будет удален из оригинального
    other_players = [p for p in room.players if p.id != player.id]
    
    for p in other_players:
        try:
            bot.send_message(p.telegram_id, notification_text, parse_mode='HTML')
        except APIError as e:
            logging.warning(f"Не удалось уведомить игрока {p.id} о выходе {player.id}: {e}")

    # Убираем игрока из комнаты
    player.current_room_id = None
    
    # Декоратор сам сделает commit
    bot.send_message(message.chat.id, "🚪 Вы успешно покинули комнату.")


@player_required
def handle_rating(bot: TeleBot, message: Message, session: Session, player: Player):
    """
    Обрабатывает команду /rating.
    Показывает статистику побед и поражений игрока.
    """
    logging.info(f"Игрок {player.username} запросил свой рейтинг.")
    
    rating_text = (
        f"<b>📊 Ваш рейтинг:</b>\n\n"
        f"🏆 <b>Побед:</b> {player.wins}\n"
        f"💀 <b>Поражений:</b> {player.losses}"
    )
    bot.send_message(message.chat.id, rating_text, parse_mode='HTML')


@player_required
def handle_achievements(bot: TeleBot, message: Message, session: Session, player: Player):
    """
    Обрабатывает команду /achievements.
    Показывает полученные игроком достижения.
    """
    logging.info(f"Игрок {player.username} запросил свои достижения.")
    
    # Используем joinedload для эффективной загрузки связанных данных об ачивках
    player_with_achievements = session.query(Player).options(
        joinedload(Player.achievements).joinedload(PlayerAchievement.achievement)
    ).filter(Player.id == player.id).one()

    achievements_text = _get_achievements_text(player_with_achievements.achievements)
    bot.send_message(message.chat.id, achievements_text, parse_mode='HTML')