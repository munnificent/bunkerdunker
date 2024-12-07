# handlers/start_handler.py

from database import Session
from models import Player
import logging

def handle_start(bot, message):
    logging.info(f"Пользователь {message.from_user.id} вызвал команду /start")
    session = Session()
    try:
        telegram_id = message.from_user.id
        username = message.from_user.username or message.from_user.first_name

        player = session.query(Player).filter_by(telegram_id=telegram_id).first()
        if not player:
            player = Player(telegram_id=telegram_id, username=username)
            session.add(player)
            session.commit()

        bot.send_message(
            message.chat.id,
            f"👋 Привет, <b>{username}</b>! Добро пожаловать в игру <b>'Бункер'</b>.\n\n"
            "Используйте /help для просмотра команд.",
            parse_mode='HTML'
        )
    except Exception as e:
        session.rollback()
        bot.send_message(message.chat.id, "Произошла ошибка при обработке вашего запроса.")
        logging.error(f"Ошибка в handle_start: {e}")
    finally:
        session.close()
