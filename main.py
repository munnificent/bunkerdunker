# main.py

import logging
import time
from telebot import TeleBot
from telebot.types import Message, CallbackQuery

from config import TOKEN
from database import init_db
from handlers import (
    start_handler, help_handler, create_room_handler,
    join_room_handler, game_handlers, admin_handlers, chat_handlers
)

# --- Инициализация и настройка ---

# Настройка логирования для отслеживания работы и ошибок бота
logging.basicConfig(
    filename='bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

bot = TeleBot(TOKEN)

# Словарь для отслеживания времени последнего действия пользователя (для защиты от спама)
user_last_action = {}


# --- Глобальный обработчик ошибок ---
def handle_errors(exception: Exception):
    """
    Глобальный обработчик для всех непредвиденных ошибок.
    Логирует ошибку и предотвращает падение бота.
    """
    logging.error(f"Произошла непредвиденная ошибка: {exception}", exc_info=True)
    # В реальном проекте можно добавить отправку уведомления администратору
    return True # Говорим библиотеке, что ошибка обработана и можно продолжать работу

# Присваиваем нашу функцию-обработчик боту.
# Это правильный способ регистрации, вместо декоратора.
bot.exception_handler = handle_errors


# --- Декораторы и вспомогательные функции ---

def rate_limit(limit_seconds: int):
    """
    Декоратор для ограничения частоты вызова команд пользователем.
    """
    def decorator(func):
        def wrapper(message: Message, *args, **kwargs):
            user_id = message.from_user.id
            current_time = time.time()
            last_action_time = user_last_action.get(user_id, 0)

            if current_time - last_action_time < limit_seconds:
                logging.warning(f"Пользователь {user_id} спамит команду.")
                bot.send_message(message.chat.id, "⏳ Пожалуйста, не отправляйте команды слишком часто.")
                return

            user_last_action[user_id] = current_time
            return func(message, *args, **kwargs)
        return wrapper
    return decorator


# --- Регистрация обработчиков ---

# Структура для удобной регистрации всех команд
COMMAND_HANDLERS = [
    # Команда, Обработчик, Ограничение частоты (сек)
    ('start', start_handler.handle_start, 2),
    ('help', help_handler.handle_help, 2),
    ('create_room', create_room_handler.handle_create_room, 5),
    ('join_room', join_room_handler.handle_join_room, 5),
    ('start_game', admin_handlers.handle_start_game, 10),
    ('kick', admin_handlers.handle_kick_player, 3),
    ('stop_game', admin_handlers.handle_stop_game, 10),
    ('start_discussion', admin_handlers.handle_start_discussion, 5),
    ('end_discussion', admin_handlers.handle_end_discussion, 5),
    ('vote', lambda b, m: admin_handlers.handle_vote_command(b, m.chat.id), 5),
    ('show_status', game_handlers.handle_show_status, 2),
    ('leave_room', game_handlers.handle_leave_room, 5),
    ('timer', admin_handlers.handle_timer, 5),
    ('rating', game_handlers.handle_rating, 2),
    ('achievements', game_handlers.handle_achievements, 2),
    ('msg', chat_handlers.handle_send_message, 2),
    ('pm', chat_handlers.handle_send_private_message, 2),
]

def register_command_handlers():
    """Регистрирует все обработчики команд из списка COMMAND_HANDLERS."""
    for command, handler, rate in COMMAND_HANDLERS:
        # Применяем декоратор rate_limit и регистрируем обработчик
        bot.message_handler(commands=[command])(
            rate_limit(rate)(
                # Оборачиваем хендлер, чтобы он принимал (bot, message)
                lambda msg, h=handler: h(bot, msg)
            )
        )

# Обработчик для кнопок голосования
@bot.callback_query_handler(func=lambda call: call.data.startswith('vote_'))
def handle_vote_callback(call: CallbackQuery):
    admin_handlers.handle_vote_callback(bot, call)


# --- Запуск бота ---

if __name__ == '__main__':
    try:
        init_db()
        register_command_handlers()
        print("Бот успешно запущен...")
        logging.info("Бот запущен.")
        bot.polling(non_stop=True, interval=1)
    except Exception as e:
        print(f"Ошибка при запуске бота: {e}")
        logging.critical(f"Критическая ошибка при запуске бота: {e}", exc_info=True)