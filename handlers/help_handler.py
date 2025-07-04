# handlers/help_handler.py

from telebot import TeleBot
from telebot.types import Message

# Текст справки вынесен в константу для лучшей читаемости и организации кода.
HELP_TEXT = """
<b>Список доступных команд:</b>

/start — Начать работу с ботом и зарегистрироваться.
/help — Показать это сообщение с описанием команд.

<b>Комнаты и игра:</b>
/create_room — Создать новую игровую комнату.
/join_room <code>[код]</code> — Присоединиться к комнате по коду.
/leave_room — Покинуть текущую комнату.

<b>Игровые действия:</b>
/show_status — Показать свои текущие характеристики.
/vote — Начать голосование за исключение игрока.
/rating — Показать свой рейтинг (победы/поражения).
/achievements — Показать свои достижения.

<b>Общение:</b>
/msg <code>[сообщение]</code> — Отправить сообщение всем в комнате.
/pm <code>[имя] [сообщение]</code> — Отправить приватное сообщение игроку.

<b>Команды хоста:</b>
/start_game — Начать игру в созданной комнате.
/stop_game — Принудительно завершить игру.
/kick <code>[имя]</code> — Исключить игрока из комнаты.
/timer <code>[минуты]</code> — Запустить таймер на обсуждение.
"""


def handle_help(bot: TeleBot, message: Message):
    """
    Обрабатывает команду /help.

    Отправляет пользователю отформатированное сообщение со списком
    всех доступных команд и их кратким описанием.
    """
    bot.send_message(message.chat.id, HELP_TEXT, parse_mode='HTML')