# handlers/chat_handlers.py

from database import Session
from models import Player, Room, Message
import logging

def get_player(session, telegram_id):
    return session.query(Player).filter_by(telegram_id=telegram_id).first()

def handle_send_message(bot, message):
    logging.info(f"Пользователь {message.from_user.id} вызвал команду /msg")
    session = Session()
    try:
        player = get_player(session, message.from_user.id)
        if not player or not player.current_room_id:
            bot.send_message(message.chat.id, "❗ Вы не находитесь в игре.")
            return

        room = session.query(Room).filter_by(id=player.current_room_id).first()
        text = message.text.partition(' ')[2]
        if not text:
            bot.send_message(message.chat.id, "❗ Введите сообщение после команды.")
            return

        new_message = Message(
            room_id=room.id,
            sender_id=player.id,
            content=text
        )
        session.add(new_message)
        session.commit()

        # Отправляем сообщение всем игрокам в комнате
        for p in room.players:
            if p.id != player.id:
                bot.send_message(p.telegram_id, f"💬 <b>{player.username}:</b> {text}", parse_mode='HTML')
        bot.send_message(message.chat.id, "✅ Сообщение отправлено всем игрокам в комнате.")
    except Exception as e:
        bot.send_message(message.chat.id, "Произошла ошибка при отправке сообщения.")
        logging.error(f"Ошибка в handle_send_message: {e}")
    finally:
        session.close()

def handle_send_private_message(bot, message):
    logging.info(f"Пользователь {message.from_user.id} вызвал команду /pm")
    session = Session()
    try:
        player = get_player(session, message.from_user.id)
        if not player or not player.current_room_id:
            bot.send_message(message.chat.id, "❗ Вы не находитесь в игре.")
            return

        args = message.text.split(' ', 2)
        if len(args) < 3:
            bot.send_message(message.chat.id, "❗ Использование: /pm [username] [сообщение]")
            return

        recipient_username = args[1]
        text = args[2]

        recipient = session.query(Player).filter_by(username=recipient_username).first()
        if not recipient or recipient.current_room_id != player.current_room_id:
            bot.send_message(message.chat.id, "❗ Игрок не найден в вашей комнате.")
            return

        new_message = Message(
            room_id=player.current_room_id,
            sender_id=player.id,
            recipient_id=recipient.id,
            content=text
        )
        session.add(new_message)
        session.commit()

        bot.send_message(recipient.telegram_id, f"🔒 <b>Приватное сообщение от {player.username}:</b> {text}", parse_mode='HTML')
        bot.send_message(message.chat.id, "✅ Приватное сообщение отправлено.")
    except Exception as e:
        bot.send_message(message.chat.id, "Произошла ошибка при отправке приватного сообщения.")
        logging.error(f"Ошибка в handle_send_private_message: {e}")
    finally:
        session.close()
