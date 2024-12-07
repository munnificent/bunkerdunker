# handlers/create_room_handler.py

from database import Session
from models import Player, Room
from utils.game_utils import generate_unique_room_code
from config import DEFAULT_MAX_PLAYERS, DEFAULT_SURVIVORS
import logging

def handle_create_room(bot, message):
    logging.info(f"Пользователь {message.from_user.id} вызвал команду /create_room")
    session = Session()
    try:
        telegram_id = message.from_user.id
        username = message.from_user.username or message.from_user.first_name

        player = session.query(Player).filter_by(telegram_id=telegram_id).first()
        if not player:
            player = Player(telegram_id=telegram_id, username=username)
            session.add(player)
            session.commit()

        if player.current_room_id:
            bot.send_message(message.chat.id, "❗ Вы уже находитесь в комнате. Сначала покиньте ее с помощью /leave_room.")
            return

        room_code = generate_unique_room_code()

        room = Room(
            code=room_code,
            host_id=player.id,
            max_players=DEFAULT_MAX_PLAYERS,
            survivors=DEFAULT_SURVIVORS
        )
        room.players.append(player)
        session.add(room)
        session.commit()

        player.current_room_id = room.id
        session.commit()

        bot.send_message(
            message.chat.id,
            f"🚪 Комната создана!\n\n<b>Код комнаты:</b> <code>{room_code}</code>\n"
            "Вы назначены хостом. Используйте /start_game для начала игры.",
            parse_mode='HTML'
        )
    except Exception as e:
        session.rollback()
        bot.send_message(message.chat.id, "Произошла ошибка при создании комнаты.")
        logging.error(f"Ошибка в handle_create_room: {e}")
    finally:
        session.close()
