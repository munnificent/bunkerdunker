# handlers/chat_handlers.py

import logging
from functools import wraps
from typing import List

from sqlalchemy.orm import Session
from telebot import TeleBot
from telebot.types import Message, APIError

from database import Session as DbSession
from models import Player, Room, Message as MessageModel

# --- Вспомогательные функции и декораторы ---

def player_in_room_required(func):
    """
    Декоратор для проверки, находится ли игрок в активной комнате.
    - Управляет сессией БД (commit, rollback, close).
    - Выполняет все стандартные проверки игрока и комнаты.
    - Передает в функцию bot, message, session, player и room.
    """
    @wraps(func)
    def wrapper(bot: TeleBot, message: Message, *args, **kwargs):
        session = DbSession()
        try:
            player = session.query(Player).filter_by(telegram_id=message.from_user.id).first()

            if not player:
                bot.send_message(message.chat.id, "❗ Вы не зарегистрированы. Используйте /start.")
                return

            if not player.current_room_id:
                bot.send_message(message.chat.id, "❗ Вы не находитесь в игровой комнате.")
                return
            
            room = session.query(Room).filter_by(id=player.current_room_id, is_active=True).first()

            if not room:
                 bot.send_message(message.chat.id, "❗ Комната, в которой вы были, больше не активна.")
                 player.current_room_id = None
                 session.commit()
                 return
            
            # Вызываем основную функцию
            result = func(bot, message, session, player, room, *args, **kwargs)
            session.commit()
            return result

        except Exception as e:
            logging.error(f"Ошибка в команде игрока '{func.__name__}': {e}", exc_info=True)
            session.rollback()
            bot.send_message(message.chat.id, "❌ Произошла непредвиденная ошибка при выполнении команды.")
        finally:
            session.close()

    return wrapper

def _broadcast_to_room(bot: TeleBot, sender: Player, room: Room, text: str):
    """Отправляет сообщение всем игрокам в комнате, кроме отправителя."""
    full_message = f"💬 <b>{sender.username}:</b> {text}"
    for p in room.players:
        if p.id != sender.id:
            try:
                bot.send_message(p.telegram_id, full_message, parse_mode='HTML')
            except APIError as e:
                logging.error(f"Не удалось отправить сообщение игроку {p.id} ({p.username}): {e}")

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
    _broadcast_to_room(bot, player, room, text)
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
    except APIError as e:
        logging.error(f"Не удалось отправить приватное сообщение от {player.username} к {recipient.username}: {e}")
        bot.send_message(message.chat.id, f"❌ Не удалось доставить сообщение игроку <b>{recipient_username}</b>. Возможно, он заблокировал бота.", parse_mode='HTML')