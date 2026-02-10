# utils/messaging_utils.py

import logging
from typing import List
from telebot import TeleBot
from models import Player


def broadcast_message(bot: TeleBot, players: List[Player], text: str, **kwargs):
    """
    Отправляет сообщение всем игрокам из списка.
    
    Args:
        bot: Экземпляр TeleBot для отправки сообщений.
        players: Список игроков-получателей.
        text: Текст сообщения для отправки.
        **kwargs: Дополнительные параметры для bot.send_message (например, parse_mode='HTML').
    """
    for player in players:
        try:
            bot.send_message(player.telegram_id, text, **kwargs)
        except Exception as e:
            logging.error(f"Не удалось отправить сообщение игроку {player.id} ({player.username}): {e}")


def broadcast_to_room_except_sender(bot: TeleBot, sender: Player, players: List[Player], text: str, **kwargs):
    """
    Отправляет сообщение всем игрокам в комнате, кроме отправителя.
    
    Args:
        bot: Экземпляр TeleBot для отправки сообщений.
        sender: Игрок-отправитель, которому не нужно отправлять сообщение.
        players: Список всех игроков в комнате.
        text: Текст сообщения для отправки.
        **kwargs: Дополнительные параметры для bot.send_message (например, parse_mode='HTML').
    """
    for player in players:
        if player.id != sender.id:
            try:
                bot.send_message(player.telegram_id, text, **kwargs)
            except Exception as e:
                logging.error(f"Не удалось отправить сообщение игроку {player.id} ({player.username}): {e}")
