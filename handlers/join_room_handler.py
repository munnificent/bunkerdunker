# handlers/join_room_handler.py

from database import Session
from models import Player, Room
import logging

def handle_join_room(bot, message):
    logging.info(f"Пользователь {message.from_user.id} вызвал команду /join_room")
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

        try:
            room_code = message.text.split()[1]
        except IndexError:
            bot.send_message(message.chat.id, "❗ Пожалуйста, укажите код комнаты после команды.")
            return

        room = session.query(Room).filter_by(code=room_code).first()
        if not room:
            bot.send_message(message.chat.id, "❗ Комната с таким кодом не найдена.")
            return

        if not room.is_active:
            bot.send_message(message.chat.id, "❗ Эта комната больше не активна.")
            return

        if len(room.players) >= room.max_players:
            bot.send_message(message.chat.id, "❗ Комната заполнена.")
            return

        room.players.append(player)
        player.current_room_id = room.id
        session.commit()

        bot.send_message(message.chat.id, f"🔑 Вы присоединились к комнате <code>{room_code}</code>!", parse_mode='HTML')
        for p in room.players:
            if p.telegram_id != telegram_id:
                bot.send_message(p.telegram_id, f"👤 Игрок <b>{player.username}</b> присоединился к комнате.", parse_mode='HTML')
    except Exception as e:
        session.rollback()
        bot.send_message(message.chat.id, "Произошла ошибка при присоединении к комнате.")
        logging.error(f"Ошибка в handle_join_room: {e}")
    finally:
        session.close()
