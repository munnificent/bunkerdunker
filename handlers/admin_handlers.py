# handlers/admin_handlers.py

import logging
import threading
import time
from functools import wraps
from typing import List

from sqlalchemy.orm import Session
from telebot import TeleBot
from telebot.types import Message, CallbackQuery

from database import Session as DbSession
from models import Player, Room, Vote, Characteristic
from utils.achievement_utils import award_new_achievements
from utils.game_utils import (
    assign_new_characteristics_to_player,
    get_random_location,
    get_random_event,
    get_random_ending,
)
from utils.markup_utils import create_voting_buttons, CB_VOTE_PREFIX

# --- Вспомогательные функции и декораторы ---

def host_required(func):
    """
    Декоратор для проверки, является ли пользователь хостом активной комнаты.
    - Создает сессию БД и управляет ею (commit, rollback, close).
    - Выполняет все стандартные проверки.
    - Передает в функцию bot, message, session, player и room.
    """
    @wraps(func)
    def wrapper(bot: TeleBot, message: Message, *args, **kwargs):
        session = DbSession()
        try:
            player = session.query(Player).filter_by(telegram_id=message.from_user.id).first()

            if not player:
                bot.send_message(message.chat.id, "❗ Вы не зарегистрированы. Используйте /start для начала.")
                return

            if not player.current_room_id:
                bot.send_message(message.chat.id, "❗ Вы не находитесь в комнате.")
                return
            
            room = session.query(Room).filter_by(id=player.current_room_id).first()

            if not room:
                 bot.send_message(message.chat.id, "❗ Комната, в которой вы были, больше не существует.")
                 player.current_room_id = None
                 session.commit()
                 return

            if room.host_id != player.id:
                bot.send_message(message.chat.id, "❗ Эту команду может использовать только хост комнаты.")
                return
            
            # Вызываем основную функцию с нужными аргументами
            result = func(bot, message, session, player, room, *args, **kwargs)
            session.commit()
            return result

        except Exception as e:
            logging.error(f"Ошибка в команде хоста '{func.__name__}': {e}", exc_info=True)
            session.rollback()
            bot.send_message(message.chat.id, "❌ Произошла непредвиденная ошибка при выполнении команды.")
        finally:
            session.close()

    return wrapper

def _broadcast_message(bot: TeleBot, players: List[Player], text: str, **kwargs):
    """Отправляет сообщение всем игрокам из списка."""
    for p in players:
        try:
            bot.send_message(p.telegram_id, text, **kwargs)
        except Exception as e: # <-- Заменено на общее исключение
            logging.error(f"Не удалось отправить сообщение игроку {p.id} ({p.username}): {e}")

# --- Обработчики команд ---

@host_required
def handle_start_game(bot: TeleBot, message: Message, session: Session, player: Player, room: Room):
    """Начинает игру, раздает характеристики и объявляет катастрофу."""
    logging.info(f"Хост {player.username} ({player.id}) начинает игру в комнате {room.code}.")
    
    if len(room.players) < 2:
        bot.send_message(message.chat.id, "❗ Недостаточно игроков для начала игры (минимум 2).")
        return

    # Назначаем характеристики и генерируем локацию
    for p in room.players:
        assign_new_characteristics_to_player(session, p)
    
    room.location = get_random_location(session)
    if not room.location:
        bot.send_message(message.chat.id, "❌ Не удалось загрузить локацию. Проверьте, заполнена ли база данных.")
        return

    # Отправляем информацию игрокам
    _send_initial_game_info(bot, room)
    
    bot.send_message(message.chat.id, "🎮 Игра началась! Используйте /start_discussion, чтобы начать обсуждение.")

def _send_initial_game_info(bot: TeleBot, room: Room):
    """Рассылает игрокам их характеристики и информацию о катастрофе."""
    location_text = (
        f"<b>Описание катастрофы:</b>\n{room.location.description}\n\n"
        f"<b>Условия для выживания:</b>\n{room.location.survival_conditions}"
    )
    
    for p in room.players:
        char_text = (
            f"<b>Ваши характеристики:</b>\n"
            f"👤 <b>Профессия:</b> {p.characteristics.profession}\n"
            f"🧬 <b>Биология:</b> {p.characteristics.biology}\n"
            f"❤️ <b>Здоровье:</b> {p.characteristics.health}\n"
            f"🎨 <b>Хобби:</b> {p.characteristics.hobby}\n"
            f"🎒 <b>Багаж:</b> {p.characteristics.luggage}\n"
            f"📜 <b>Факт:</b> {p.characteristics.facts}\n"
            f"😱 <b>Фобия:</b> {p.characteristics.phobia}\n"
            f"✨ <b>Талант:</b> {p.characteristics.talent}\n"
            f"🏷️ <b>Соц. статус:</b> {p.characteristics.social_status}"
        )
        _broadcast_message(bot, [p], char_text, parse_mode='HTML')
        _broadcast_message(bot, [p], location_text, parse_mode='HTML')

@host_required
def handle_kick_player(bot: TeleBot, message: Message, session: Session, player: Player, room: Room):
    """Исключает игрока из комнаты по команде хоста."""
    try:
        username_to_kick = message.text.split()[1]
    except IndexError:
        bot.send_message(message.chat.id, "❗ Укажите имя пользователя для исключения. Пример: /kick <username>")
        return

    player_to_kick = next((p for p in room.players if p.username == username_to_kick), None)

    if not player_to_kick:
        bot.send_message(message.chat.id, f"❗ Игрок с именем <b>{username_to_kick}</b> не найден в комнате.", parse_mode='HTML')
        return
    
    if player_to_kick.id == player.id:
        bot.send_message(message.chat.id, "❗ Вы не можете исключить самого себя.")
        return

    # Исключаем игрока
    player_to_kick.current_room_id = None
    logging.info(f"Игрок {player_to_kick.username} был исключен из комнаты {room.code} хостом {player.username}.")
    
    _broadcast_message(bot, room.players, f"👤 Игрок <b>{player_to_kick.username}</b> был исключен хостом.", parse_mode='HTML')
    bot.send_message(player_to_kick.telegram_id, "❗ Вы были исключены из комнаты хостом.")

@host_required
def handle_stop_game(bot: TeleBot, message: Message, session: Session, player: Player, room: Room):
    """Принудительно завершает игру в комнате."""
    logging.warning(f"Хост {player.username} принудительно завершил игру в комнате {room.code}.")
    _cleanup_room(bot, room, "⛔ Игра была принудительно завершена хостом.")

@host_required
def handle_start_discussion(bot: TeleBot, message: Message, session: Session, player: Player, room: Room):
    """Начинает раунд обсуждения."""
    room.is_voting = False
    _broadcast_message(bot, room.players, "💬 Обсуждение началось! Расскажите о себе и решите, кто должен остаться.")

@host_required
def handle_end_discussion(bot: TeleBot, message: Message, session: Session, player: Player, room: Room):
    """Завершает раунд обсуждения и запускает голосование."""
    _start_voting_round(bot, room)

def handle_vote_command(bot: TeleBot, chat_id: int):
    """Обрабатывает команду /vote от игрока."""
    session = DbSession()
    try:
        player = session.query(Player).filter_by(telegram_id=chat_id).first()
        if not player or not player.current_room_id:
            bot.send_message(chat_id, "❗ Вы не находитесь в активной игре.")
            return

        room = session.query(Room).filter_by(id=player.current_room_id).first()
        if not room.is_voting:
            bot.send_message(chat_id, "❗ Сейчас не время для голосования.")
            return

        # Проверяем, не голосовал ли игрок уже
        existing_vote = session.query(Vote).filter_by(room_id=room.id, voter_id=player.id).first()
        if existing_vote:
            bot.send_message(chat_id, "❗ Вы уже проголосовали в этом раунде.")
            return
        
        players_to_vote_for = [p for p in room.players if p.id != player.id]
        markup = create_voting_buttons(players_to_vote_for)
        bot.send_message(chat_id, "🗳️ Выберите игрока, которого вы хотите исключить:", reply_markup=markup)
    finally:
        session.close()

def handle_vote_callback(bot: TeleBot, call: CallbackQuery):
    """Обрабатывает нажатие на кнопку голосования."""
    session = DbSession()
    try:
        voter = session.query(Player).filter_by(telegram_id=call.from_user.id).first()
        if not voter or not voter.current_room_id:
            bot.answer_callback_query(call.id, "❗ Вы не находитесь в игре.", show_alert=True)
            return

        room = session.query(Room).filter_by(id=voter.current_room_id).first()
        if not room.is_voting:
            bot.answer_callback_query(call.id, "❗ Голосование уже завершено.", show_alert=True)
            return
        
        # Проверяем, не голосовал ли игрок уже
        if session.query(Vote).filter_by(room_id=room.id, voter_id=voter.id).count() > 0:
            bot.answer_callback_query(call.id, "❗ Вы уже проголосовали!", show_alert=True)
            return

        voted_player_tid = int(call.data.replace(CB_VOTE_PREFIX, ''))
        voted_player = session.query(Player).filter_by(telegram_id=voted_player_tid).first()

        # Создаем и сохраняем голос
        vote = Vote(room_id=room.id, voter_id=voter.id, voted_player_id=voted_player.id)
        session.add(vote)
        session.commit()
        bot.answer_callback_query(call.id, "✅ Ваш голос учтен!")
        bot.edit_message_text("✅ Ваш голос учтен!", call.message.chat.id, call.message.message_id)

        # Проверяем, все ли проголосовали
        if session.query(Vote).filter_by(room_id=room.id).count() == len(room.players):
            _handle_vote_results(bot, room, session)

    except Exception as e:
        logging.error(f"Ошибка в vote_callback: {e}", exc_info=True)
        bot.answer_callback_query(call.id, "❌ Ошибка при обработке голоса.", show_alert=True)
        session.rollback()
    finally:
        session.close()

def _handle_vote_results(bot: TeleBot, room: Room, session: Session):
    """Подсчитывает голоса и обрабатывает результаты."""
    votes = session.query(Vote.voted_player_id).filter_by(room_id=room.id).all()
    vote_counts = {pid[0]: votes.count(pid) for pid in set(votes)}
    
    max_votes = max(vote_counts.values())
    players_with_max_votes = [pid for pid, count in vote_counts.items() if count == max_votes]

    # Очищаем голоса предыдущего раунда
    session.query(Vote).filter_by(room_id=room.id).delete()
    
    if len(players_with_max_votes) > 1:
        _broadcast_message(bot, room.players, "⚖️ Ничья при голосовании! Начинается раунд переголосования.")
        _start_voting_round(bot, room)
        return

    excluded_player = session.query(Player).get(players_with_max_votes[0])
    
    # Показываем характеристики исключенного игрока
    char_text = f"<b>Характеристики исключенного игрока {excluded_player.username}:</b>\n" + \
                f"👤 <b>Профессия:</b> {excluded_player.characteristics.profession}\n" #... и т.д.
    _broadcast_message(bot, room.players, char_text, parse_mode='HTML')
    
    excluded_player.current_room_id = None
    _broadcast_message(bot, room.players, f"🚫 Игрок <b>{excluded_player.username}</b> был исключен из бункера.", parse_mode='HTML')
    bot.send_message(excluded_player.telegram_id, "❗ Вы были исключены из бункера.")

    if len(room.players) <= room.survivors:
        _process_game_end(bot, room, session)
    else:
        _broadcast_message(bot, [room.host], "💬 Используйте /start_discussion для начала следующего раунда.")
        trigger_random_event(bot, room)

def _process_game_end(bot: TeleBot, room: Room, session: Session):
    """Обрабатывает завершение игры, начисляет статистику и достижения."""
    survivors = list(room.players)
    all_players_in_game = session.query(Player).filter(Player.id.in_([p.id for p in survivors])).all() # Перезапрос для актуальности
    
    winner_usernames = [p.username for p in survivors]
    winners_text = f"🎉 <b>Игра завершена!</b>\n\n<b>Выжившие игроки:</b>\n" + "\n".join(winner_usernames)
    
    _broadcast_message(bot, survivors, winners_text, parse_mode='HTML')
    _broadcast_message(bot, survivors, get_random_ending(), parse_mode='HTML')

    # Обновляем статистику победителей
    for survivor in survivors:
        survivor.wins += 1
        award_new_achievements(bot, survivor, session)
        
    # Ищем всех, кто был в комнате, но не выжил
    losers = session.query(Player).filter(
        Player.current_room_id == room.id, 
        Player.id.notin_([p.id for p in survivors])
    ).all()
    
    for loser in losers:
        loser.losses += 1
        award_new_achievements(bot, loser, session)

    _cleanup_room(bot, room, "Игра окончена. Спасибо за участие!")
    
def _cleanup_room(bot: TeleBot, room: Room, final_message: str):
    """Очищает комнату и распускает игроков."""
    _broadcast_message(bot, room.players, final_message)
    
    for p in list(room.players):
        p.current_room_id = None
        
    room.is_active = False

def _start_voting_round(bot: TeleBot, room: Room):
    """Инициирует новый раунд голосования."""
    room.is_voting = True
    _broadcast_message(bot, room.players, "🗳️ Обсуждение завершено! Начинается голосование. Используйте /vote, чтобы сделать свой выбор.")

def trigger_random_event(bot: TeleBot, room: Room):
    """Отправляет случайное событие всем игрокам в комнате."""
    event = get_random_event()
    _broadcast_message(bot, room.players, f"🔔 <b>Случайное событие:</b>\n{event}", parse_mode='HTML')

@host_required
def handle_timer(bot: TeleBot, message: Message, session: Session, player: Player, room: Room):
    """Устанавливает таймер обсуждения."""
    try:
        minutes = int(message.text.split()[1])
        if not 1 <= minutes <= 60:
            raise ValueError
    except (IndexError, ValueError):
        bot.send_message(message.chat.id, "❗ Укажите время в минутах (от 1 до 60). Пример: /timer 5")
        return

    _broadcast_message(bot, room.players, f"⏰ Хост запустил таймер на {minutes} минут.")
    
    # Запуск таймера в отдельном потоке
    threading.Thread(target=_timer_countdown, args=(bot, room.id, minutes), daemon=True).start()

def _timer_countdown(bot: TeleBot, room_id: int, minutes: int):
    """Функция обратного отсчета для таймера."""
    time.sleep(minutes * 60)
    session = DbSession()
    try:
        room = session.query(Room).filter_by(id=room_id, is_active=True).first()
        if not room:
            logging.info(f"Таймер для комнаты {room_id} завершился, но комната уже неактивна.")
            return

        _broadcast_message(bot, room.players, f"⏰ Время обсуждения ({minutes} мин) истекло!")
        _start_voting_round(bot, room)
        session.commit()
    except Exception as e:
        logging.error(f"Ошибка в потоке таймера для комнаты {room_id}: {e}", exc_info=True)
        session.rollback()
    finally:
        session.close()