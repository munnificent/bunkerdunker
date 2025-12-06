# handlers/join_room_handler.py

import logging
from telebot import TeleBot
from telebot.types import Message
from sqlalchemy.orm import Session

from models import Player, Room
from utils.decorators import player_required
from utils.messaging_utils import broadcast_to_room_except_sender

# --- Обработчик команды ---

@player_required
def handle_join_room(bot: TeleBot, message: Message, session: Session, player: Player):
    """
    Обрабатывает команду /join_room.
    Позволяет игроку присоединиться к существующей комнате по коду.
    """
    logging.info(f"Игрок {player.username} ({player.id}) пытается присоединиться к комнате.")

    if player.current_room_id:
        bot.send_message(message.chat.id, "❗ Вы уже находитесь в комнате. Сначала покиньте ее с помощью /leave_room.")
        return

    try:
        room_code = message.text.split()[1]
    except IndexError:
        bot.send_message(message.chat.id, "❗ Укажите код комнаты после команды. Пример: /join_room ABC123")
        return

    # Ищем комнату по коду
    room = session.query(Room).filter_by(code=room_code).first()

    # Последовательно проверяем все условия
    if not room:
        bot.send_message(message.chat.id, f"❗ Комната с кодом <code>{room_code}</code> не найдена.", parse_mode='HTML')
        return

    if not room.is_active:
        bot.send_message(message.chat.id, "❗ Эта игра уже завершена. Нельзя присоединиться.")
        return

    if len(room.players) >= room.max_players:
        bot.send_message(message.chat.id, "❗ К сожалению, эта комната уже заполнена.")
        return

    # Если все проверки пройдены, добавляем игрока
    player.room = room  # SQLAlchemy автоматически установит player.current_room_id
    
    # Уведомляем всех в комнате о новом игроке
    notification_text = f"👤 Игрок <b>{player.username}</b> присоединился к комнате!"
    broadcast_to_room_except_sender(bot, player, room.players, notification_text, parse_mode='HTML')

    bot.send_message(message.chat.id, f"✅ Вы успешно присоединились к комнате <code>{room_code}</code>!", parse_mode='HTML')
    logging.info(f"Игрок {player.username} присоединился к комнате {room.code}.")
    # Декоратор сам выполнит session.commit()