# handlers/game_handlers.py

import logging
from typing import List

from sqlalchemy.orm import Session, joinedload
from telebot import TeleBot
from telebot.types import Message

from models import Player, Room, Characteristic, PlayerAchievement
from utils.decorators import player_required, player_in_room_required
from utils.player_utils import format_player_characteristics
from utils.messaging_utils import broadcast_to_room_except_sender

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
    
    char_text = format_player_characteristics(player)
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
    broadcast_to_room_except_sender(bot, player, room.players, notification_text, parse_mode='HTML')

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