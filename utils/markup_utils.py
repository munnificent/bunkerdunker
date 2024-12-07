# utils/markup_utils.py

from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

def create_voting_buttons(players):
    markup = InlineKeyboardMarkup()
    for player in players:
        button = InlineKeyboardButton(player.username, callback_data=f"vote_{player.telegram_id}")
        markup.add(button)
    return markup

def create_confirmation_buttons():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("✅ Да", callback_data='confirm_yes'),
        InlineKeyboardButton("❌ Нет", callback_data='confirm_no')
    )
    return markup
