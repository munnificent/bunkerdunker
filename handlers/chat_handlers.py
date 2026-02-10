# handlers/chat_handlers.py

import logging

from sqlalchemy.orm import Session
from telebot import TeleBot
from telebot.types import Message

from models import Player, Room, Message as MessageModel
from utils.decorators import player_in_room_required
from utils.messaging_utils import broadcast_to_room_except_sender

# --- Обработчики команд ---

@player_in_room_required
def handle_send_message(bot: TeleBot, message: Message, session: Session, player: Player, room: Room):
    """
    Обрабатывает команду /msg для отправки сообщения всем игрокам в комнате.
    """
    logging.info(f"Игрок {player.username} отправил сообщение в комнату {room.code}")
    
    # Извлекаем текст сообщения, отсекая саму команду
    text = message.text.partition(' ')[2]
    if not text:
        bot.send_message(message.chat.id, "❗ Введите текст сообщения после команды. Пример: /msg Привет всем!")
        return

    # Сохраняем сообщение в БД
    new_message = MessageModel(room_id=room.id, sender_id=player.id, content=text)
    session.add(new_message)

    # Рассылаем сообщение другим игрокам
    full_message = f"💬 <b>{player.username}:</b> {text}"
    broadcast_to_room_except_sender(bot, player, room.players, full_message, parse_mode='HTML')
    bot.send_message(message.chat.id, "✅ Сообщение отправлено всем игрокам в комнате.")

@player_in_room_required
def handle_send_private_message(bot: TeleBot, message: Message, session: Session, player: Player, room: Room):
    """
    Обрабатывает команду /pm для отправки приватного сообщения другому игроку.
    """
    logging.info(f"Игрок {player.username} отправляет приватное сообщение в комнате {room.code}")

    args = message.text.split(' ', 2)
    if len(args) < 3:
        bot.send_message(message.chat.id, "❗ Неправильный формат. Используйте: /pm <имя_пользователя> <сообщение>")
        return

    recipient_username, text = args[1], args[2]

    if recipient_username == player.username:
        bot.send_message(message.chat.id, "❗ Вы не можете отправить приватное сообщение самому себе.")
        return

    # Ищем получателя в той же комнате
    recipient = next((p for p in room.players if p.username == recipient_username), None)
    if not recipient:
        bot.send_message(message.chat.id, f"❗ Игрок с именем <b>{recipient_username}</b> не найден в вашей комнате.", parse_mode='HTML')
        return

    # Сохраняем сообщение в БД
    new_message = MessageModel(
        room_id=room.id,
        sender_id=player.id,
        recipient_id=recipient.id,
        content=text
    )
    session.add(new_message)

    # Отправляем приватное сообщение
    try:
        private_text = f"🔒 <b>Приватное сообщение от {player.username}:</b> {text}"
        bot.send_message(recipient.telegram_id, private_text, parse_mode='HTML')
        bot.send_message(message.chat.id, f"✅ Приватное сообщение для <b>{recipient_username}</b> отправлено.", parse_mode='HTML')
    except Exception as e: # <-- Заменено на общее исключение
        logging.error(f"Не удалось отправить приватное сообщение от {player.username} к {recipient.username}: {e}")
        bot.send_message(message.chat.id, f"❌ Не удалось доставить сообщение игроку <b>{recipient_username}</b>. Возможно, он заблокировал бота.", parse_mode='HTML')