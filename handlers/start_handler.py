# handlers/start_handler.py

import logging
from telebot import TeleBot
from telebot.types import Message
from sqlalchemy.orm import Session

from models import Player
from utils.decorators import player_required


# --- Обработчик команды ---

@player_required
def handle_start(bot: TeleBot, message: Message, session: Session, player: Player):
    """
    Обрабатывает команду /start.

    Регистрирует нового пользователя или приветствует существующего.
    Декоратор @player_required управляет созданием/поиском игрока и сессией БД.
    """
    logging.info(f"Игрок {player.username} ({player.id}) запустил бота.")
    
    welcome_text = (
        f"👋 Привет, <b>{player.username}</b>! Добро пожаловать в игру <b>'Бункер'</b>.\n\n"
        "Я помогу вам провести игру: раздам характеристики, проведу голосование и определю победителей.\n\n"
        "Используйте /help, чтобы увидеть список всех доступных команд."
    )
    
    bot.send_message(
        message.chat.id,
        welcome_text,
        parse_mode='HTML'
    )