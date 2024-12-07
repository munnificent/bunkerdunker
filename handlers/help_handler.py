# handlers/help_handler.py

def handle_help(bot, message):
    help_text = """
<b>Список доступных команд:</b>
/start — Начать работу с ботом.
/create_room — Создать новую игровую комнату.
/join_room [код] — Присоединиться к существующей комнате.
/leave_room — Покинуть текущую комнату.
/start_game — Начать игру (для хоста).
/stop_game — Завершить игру (для хоста).
/kick [username] — Исключить игрока (для хоста).
/vote — Проголосовать за исключение игрока.
/show_status — Показать свои характеристики.
/timer [минуты] — Запустить таймер обсуждения.
/rating — Показать свой рейтинг.
/achievements — Показать свои достижения.
/msg [сообщение] — Отправить сообщение всем игрокам в комнате.
/pm [username] [сообщение] — Отправить приватное сообщение игроку.
/help — Показать это сообщение.
"""
    bot.send_message(message.chat.id, help_text, parse_mode='HTML')
