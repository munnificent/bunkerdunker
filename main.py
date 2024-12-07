# main.py

import telebot
from config import TOKEN
from database import init_db
from handlers import (
    start_handler, help_handler, create_room_handler,
    join_room_handler, game_handlers, admin_handlers, chat_handlers
)
from telebot.types import Message, CallbackQuery
import logging
import time

bot = telebot.TeleBot(TOKEN)

# Настройка логирования
logging.basicConfig(
    filename='bot.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

# Ограничение частоты команд
users_last_action = {}

def rate_limit(limit):
    def decorator(func):
        def wrapper(message, *args, **kwargs):
            user_id = message.from_user.id
            current_time = time.time()
            last_action = users_last_action.get(user_id, 0)
            if current_time - last_action < limit:
                bot.send_message(message.chat.id, "⏳ Пожалуйста, не спамьте командами.")
                return
            users_last_action[user_id] = current_time
            return func(message, *args, **kwargs)
        return wrapper
    return decorator

# Инициализация базы данных
init_db()

# Обработчики команд
@bot.message_handler(commands=['start'])
@rate_limit(2)
def handle_start(message: Message):
    start_handler.handle_start(bot, message)

@bot.message_handler(commands=['help'])
@rate_limit(2)
def handle_help(message: Message):
    help_handler.handle_help(bot, message)

@bot.message_handler(commands=['create_room'])
def handle_create_room(message: Message):
    create_room_handler.handle_create_room(bot, message)

@bot.message_handler(commands=['join_room'])
def handle_join_room(message: Message):
    join_room_handler.handle_join_room(bot, message)

@bot.message_handler(commands=['start_game'])
def handle_start_game(message: Message):
    admin_handlers.handle_start_game(bot, message)

@bot.message_handler(commands=['kick'])
def handle_kick_player(message: Message):
    admin_handlers.handle_kick_player(bot, message)

@bot.message_handler(commands=['stop_game'])
def handle_stop_game(message: Message):
    admin_handlers.handle_stop_game(bot, message)

@bot.message_handler(commands=['start_discussion'])
def handle_start_discussion(message: Message):
    admin_handlers.handle_start_discussion(bot, message)

@bot.message_handler(commands=['end_discussion'])
def handle_end_discussion(message: Message):
    admin_handlers.handle_end_discussion(bot, message)

@bot.message_handler(commands=['vote'])
def handle_vote_command(message: Message):
    admin_handlers.handle_vote_command(bot, message.chat.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith('vote_'))
def handle_vote_callback(call: CallbackQuery):
    admin_handlers.handle_vote_callback(bot, call)

@bot.message_handler(commands=['show_status'])
def handle_show_status(message: Message):
    game_handlers.handle_show_status(bot, message)

@bot.message_handler(commands=['leave_room'])
def handle_leave_room(message: Message):
    game_handlers.handle_leave_room(bot, message)

@bot.message_handler(commands=['timer'])
def handle_timer(message: Message):
    admin_handlers.handle_timer(bot, message)

@bot.message_handler(commands=['rating'])
def handle_rating(message: Message):
    game_handlers.handle_rating(bot, message)

@bot.message_handler(commands=['achievements'])
def handle_achievements(message: Message):
    game_handlers.handle_achievements(bot, message)

@bot.message_handler(commands=['msg'])
def handle_send_message_command(message: Message):
    chat_handlers.handle_send_message(bot, message)

@bot.message_handler(commands=['pm'])
def handle_send_private_message_command(message: Message):
    chat_handlers.handle_send_private_message(bot, message)

if __name__ == '__main__':
    print("Бот запущен...")
    bot.polling(none_stop=True)
