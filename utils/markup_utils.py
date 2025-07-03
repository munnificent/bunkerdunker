# utils/markup_utils.py

from typing import List
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

# Локальный импорт для тайп-хинтинга, чтобы избежать циклических зависимостей
from models import Player

# --- Константы для callback_data ---
# Использование констант помогает избежать опечаток и упрощает поддержку кода.
CB_VOTE_PREFIX = 'vote_'
CB_CONFIRM_YES = 'confirm_yes'
CB_CONFIRM_NO = 'confirm_no'


def create_voting_buttons(players: List[Player]) -> InlineKeyboardMarkup:
    """
    Создает клавиатуру с кнопками для голосования за исключение игроков.

    Args:
        players: Список объектов Player, за которых можно голосовать.

    Returns:
        Объект InlineKeyboardMarkup с кнопками для голосования.
    """
    markup = InlineKeyboardMarkup()
    # Каждая кнопка будет на новой строке для удобства нажатия на мобильных устройствах.
    for player in players:
        button = InlineKeyboardButton(
            text=player.username,
            callback_data=f"{CB_VOTE_PREFIX}{player.telegram_id}"
        )
        markup.add(button)
    return markup


def create_confirmation_buttons() -> InlineKeyboardMarkup:
    """
    Создает простую клавиатуру для подтверждения действия (Да/Нет).

    Returns:
        Объект InlineKeyboardMarkup с кнопками "Да" и "Нет".
    """
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("✅ Да", callback_data=CB_CONFIRM_YES),
        InlineKeyboardButton("❌ Нет", callback_data=CB_CONFIRM_NO)
    )
    return markup