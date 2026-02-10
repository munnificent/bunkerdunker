# handlers/create_room_handler.py

import logging

from sqlalchemy.orm import Session
from telebot import TeleBot
from telebot.types import Message

from config import DEFAULT_MAX_PLAYERS, DEFAULT_SURVIVORS
from models import Player, Room
from utils.game_utils import generate_unique_room_code
from utils.decorators import player_required

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