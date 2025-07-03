# handlers/create_room_handler.py

import logging
from functools import wraps

from sqlalchemy.orm import Session
from telebot import TeleBot
from telebot.types import Message

from config import DEFAULT_MAX_PLAYERS, DEFAULT_SURVIVORS
from database import Session as DbSession
from models import Player, Room
from utils.game_utils import generate_unique_room_code

# --- Декораторы ---

def player_required(func):
    """
    Декоратор для получения или создания игрока и управления сессией БД.
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

# --- Обработчик команды ---

@player_required
def handle_create_room(bot: TeleBot, message: Message, session: Session, player: Player):
    """
    Обрабатывает команду /create_room.
    """
    logging.info(f"Игрок {player.username} ({player.id}) создает новую комнату.")

    if player.current_room_id:
        bot.send_message(message.chat.id, "❗ Вы уже находитесь в комнате. Сначала покиньте ее с помощью /leave_room.")
        return

    room_code = generate_unique_room_code(session)

    # ИСПРАВЛЕНИЕ: Создаем комнату и сразу же добавляем ее в сессию.
    new_room = Room(
        code=room_code,
        host_id=player.id, # Присваиваем ID напрямую
        max_players=DEFAULT_MAX_PLAYERS,
        survivors=DEFAULT_SURVIVORS
    )
    session.add(new_room)
    
    # ИСПРАВЛЕНИЕ: Делаем flush, чтобы получить ID новой комнаты.
    # Это позволит нам безопасно установить связь с игроком.
    session.flush()

    player.current_room_id = new_room.id
    
    # Финальный commit всех изменений будет выполнен в декораторе
    bot.send_message(
        message.chat.id,
        f"🚪 Комната успешно создана!\n\n"
        f"<b>Код для присоединения:</b> <code>{room_code}</code>\n\n"
        f"Вы — хост этой комнаты. Когда все соберутся, используйте /start_game для начала игры.",
        parse_mode='HTML'
    )