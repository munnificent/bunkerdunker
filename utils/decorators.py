# utils/decorators.py

import logging
from functools import wraps
from sqlalchemy.orm import Session
from telebot import TeleBot
from telebot.types import Message

from database import Session as DbSession
from models import Player, Room


def player_required(func):
    """
    Декоратор для получения или создания игрока и управления сессией БД.
    
    - Создает сессию БД и управляет ею (commit, rollback, close).
    - Получает или создает объект игрока по telegram_id.
    - Передает в функцию bot, message, session и player.
    """
    @wraps(func)
    def wrapper(bot: TeleBot, message: Message, *args, **kwargs):
        session = DbSession()
        try:
            telegram_id = message.from_user.id
            username = message.from_user.username or message.from_user.first_name

            player = session.query(Player).filter_by(telegram_id=telegram_id).first()
            if not player:
                player = Player(telegram_id=telegram_id, username=username)
                session.add(player)
                session.commit()
                logging.info(f"Создан новый игрок: {username} ({telegram_id}).")

            result = func(bot, message, session, player, *args, **kwargs)
            session.commit()
            return result

        except Exception as e:
            logging.error(f"Ошибка в команде '{func.__name__}': {e}", exc_info=True)
            session.rollback()
            bot.send_message(message.chat.id, "❌ Произошла непредвиденная ошибка при выполнении команды.")
        finally:
            session.close()

    return wrapper


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


def host_required(func):
    """
    Декоратор для проверки, является ли пользователь хостом активной комнаты.
    
    - Создает сессию БД и управляет ею (commit, rollback, close).
    - Выполняет все стандартные проверки.
    - Передает в функцию bot, message, session, player и room.
    """
    @wraps(func)
    def wrapper(bot: TeleBot, message: Message, *args, **kwargs):
        session = DbSession()
        try:
            player = session.query(Player).filter_by(telegram_id=message.from_user.id).first()

            if not player:
                bot.send_message(message.chat.id, "❗ Вы не зарегистрированы. Используйте /start для начала.")
                return

            if not player.current_room_id:
                bot.send_message(message.chat.id, "❗ Вы не находитесь в комнате.")
                return
            
            room = session.query(Room).filter_by(id=player.current_room_id).first()

            if not room:
                bot.send_message(message.chat.id, "❗ Комната, в которой вы были, больше не существует.")
                player.current_room_id = None
                session.commit()
                return

            if room.host_id != player.id:
                bot.send_message(message.chat.id, "❗ Эту команду может использовать только хост комнаты.")
                return
            
            # Вызываем основную функцию с нужными аргументами
            result = func(bot, message, session, player, room, *args, **kwargs)
            session.commit()
            return result

        except Exception as e:
            logging.error(f"Ошибка в команде хоста '{func.__name__}': {e}", exc_info=True)
            session.rollback()
            bot.send_message(message.chat.id, "❌ Произошла непредвиденная ошибка при выполнении команды.")
        finally:
            session.close()

    return wrapper
