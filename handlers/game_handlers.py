# handlers/game_handlers.py

from database import Session
from models import Player, Room, Characteristic, Vote, Location, Achievement, PlayerAchievement
from utils.game_utils import (
    get_random_event
)
from utils.markup_utils import create_voting_buttons
from utils.achievement_utils import check_and_award_achievements
from telebot.types import Message
import logging

def handle_show_status(bot, message):
    logging.info(f"Пользователь {message.from_user.id} вызвал команду /show_status")
    session = Session()
    try:
        telegram_id = message.from_user.id
        player = session.query(Player).filter_by(telegram_id=telegram_id).first()
        if not player:
            bot.send_message(message.chat.id, "❗ Вы не зарегистрированы. Используйте /start для начала.")
            return

        characteristics = session.query(Characteristic).filter_by(player_id=player.id).first()
        if not characteristics:
            bot.send_message(message.chat.id, "❗ У вас нет характеристик.")
            return

        char_text = f"""
<b>Ваши характеристики:</b>
👤 <b>Профессия:</b> {characteristics.profession}
🧬 <b>Биология:</b> {characteristics.biology}
❤️ <b>Здоровье:</b> {characteristics.health}
🎨 <b>Хобби:</b> {characteristics.hobby}
🎒 <b>Багаж:</b> {characteristics.luggage}
📜 <b>Факт:</b> {characteristics.facts}
😱 <b>Фобия:</b> {characteristics.phobia}
✨ <b>Талант:</b> {characteristics.talent}
🏷️ <b>Социальный статус:</b> {characteristics.social_status}
"""
        bot.send_message(message.chat.id, char_text, parse_mode='HTML')
    except Exception as e:
        bot.send_message(message.chat.id, "Произошла ошибка при получении ваших характеристик.")
        logging.error(f"Ошибка в handle_show_status: {e}")
    finally:
        session.close()

def handle_leave_room(bot, message):
    logging.info(f"Пользователь {message.from_user.id} вызвал команду /leave_room")
    session = Session()
    try:
        telegram_id = message.from_user.id
        player = session.query(Player).filter_by(telegram_id=telegram_id).first()

        if not player or not player.current_room_id:
            bot.send_message(message.chat.id, "❗ Вы не находитесь в комнате.")
            return

        room = session.query(Room).filter_by(id=player.current_room_id).first()
        room.players.remove(player)
        player.current_room_id = None

        # Удаляем характеристики игрока
        characteristics = session.query(Characteristic).filter_by(player_id=player.id).first()
        if characteristics:
            session.delete(characteristics)

        session.commit()

        bot.send_message(message.chat.id, "🚪 Вы покинули комнату.")
        for p in room.players:
            bot.send_message(p.telegram_id, f"👤 Игрок <b>{player.username}</b> покинул комнату.", parse_mode='HTML')
    except Exception as e:
        session.rollback()
        bot.send_message(message.chat.id, "Произошла ошибка при выходе из комнаты.")
        logging.error(f"Ошибка в handle_leave_room: {e}")
    finally:
        session.close()

def handle_rating(bot, message):
    logging.info(f"Пользователь {message.from_user.id} вызвал команду /rating")
    session = Session()
    try:
        telegram_id = message.from_user.id
        player = session.query(Player).filter_by(telegram_id=telegram_id).first()
        if not player:
            bot.send_message(message.chat.id, "❗ Вы не зарегистрированы. Используйте /start для начала.")
            return
        rating_text = f"""
<b>Ваш рейтинг:</b>
🏆 <b>Побед:</b> {player.wins}
💀 <b>Поражений:</b> {player.losses}
"""
        bot.send_message(message.chat.id, rating_text, parse_mode='HTML')
    except Exception as e:
        bot.send_message(message.chat.id, "Произошла ошибка при получении вашего рейтинга.")
        logging.error(f"Ошибка в handle_rating: {e}")
    finally:
        session.close()

def handle_achievements(bot, message):
    logging.info(f"Пользователь {message.from_user.id} вызвал команду /achievements")
    session = Session()
    try:
        telegram_id = message.from_user.id
        player = session.query(Player).filter_by(telegram_id=telegram_id).first()
        if not player:
            bot.send_message(message.chat.id, "❗ Вы не зарегистрированы. Используйте /start для начала.")
            return

        achievements = session.query(PlayerAchievement).filter_by(player_id=player.id).all()
        if not achievements:
            bot.send_message(message.chat.id, "🎖️ У вас пока нет достижений.")
            return

        achievement_texts = []
        for pa in achievements:
            achievement = session.query(Achievement).filter_by(id=pa.achievement_id).first()
            if achievement:
                achievement_texts.append(f"🏅 <b>{achievement.name}</b>: {achievement.description}")

        text = "<b>Ваши достижения:</b>\n" + "\n".join(achievement_texts)
        bot.send_message(message.chat.id, text, parse_mode='HTML')
    except Exception as e:
        bot.send_message(message.chat.id, "Произошла ошибка при получении ваших достижений.")
        logging.error(f"Ошибка в handle_achievements: {e}")
    finally:
        session.close()
