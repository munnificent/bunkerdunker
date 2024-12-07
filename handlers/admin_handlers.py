# handlers/admin_handlers.py

from database import Session
from models import Player, Room, Vote, Characteristic, Location, Achievement, PlayerAchievement
from utils.game_utils import (
    assign_characteristics_to_player,
    generate_location,
    get_random_event,
    get_random_ending
)
from utils.markup_utils import create_voting_buttons
from utils.achievement_utils import check_and_award_achievements
import threading
import time
import logging

def handle_start_game(bot, message):
    logging.info(f"Пользователь {message.from_user.id} вызвал команду /start_game")
    session = Session()
    try:
        telegram_id = message.from_user.id
        player = session.query(Player).filter_by(telegram_id=telegram_id).first()
        if not player:
            bot.send_message(message.chat.id, "❗ Вы не зарегистрированы. Используйте /start для начала.")
            return

        room = session.query(Room).filter_by(id=player.current_room_id).first()
        if not room or room.host_id != player.id:
            bot.send_message(message.chat.id, "❗ Вы не являетесь хостом комнаты.")
            return

        if len(room.players) < 2:
            bot.send_message(message.chat.id, "❗ Недостаточно игроков для начала игры.")
            return

        # Назначаем характеристики игрокам
        for p in room.players:
            assign_characteristics_to_player(p)

        # Генерируем локацию
        location = generate_location()
        room.location_id = location.id
        session.commit()

        # Отправляем характеристики игрокам
        for p in room.players:
            characteristics = session.query(Characteristic).filter_by(player_id=p.id).first()
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
            bot.send_message(p.telegram_id, char_text, parse_mode='HTML')

        # Отправляем информацию о локации
        location = session.query(Location).filter_by(id=room.location_id).first()
        location_text = f"""
<b>Описание катастрофы:</b>
{location.description}

<b>Условия для выживания:</b>
{location.survival_conditions}
"""
        for p in room.players:
            bot.send_message(p.telegram_id, location_text, parse_mode='HTML')

        bot.send_message(message.chat.id, "🎮 Игра началась! Используйте /start_discussion для начала обсуждения.")
    except Exception as e:
        session.rollback()
        bot.send_message(message.chat.id, "Произошла ошибка при начале игры.")
        logging.error(f"Ошибка в handle_start_game: {e}")
    finally:
        session.close()

def handle_kick_player(bot, message):
    logging.info(f"Пользователь {message.from_user.id} вызвал команду /kick")
    session = Session()
    try:
        telegram_id = message.from_user.id
        player = session.query(Player).filter_by(telegram_id=telegram_id).first()

        if not player:
            bot.send_message(message.chat.id, "❗ Вы не зарегистрированы. Используйте /start для начала.")
            return

        room = session.query(Room).filter_by(id=player.current_room_id).first()
        if not room or room.host_id != player.id:
            bot.send_message(message.chat.id, "❗ Вы не являетесь хостом комнаты.")
            return

        try:
            username = message.text.split()[1]
        except IndexError:
            bot.send_message(message.chat.id, "❗ Пожалуйста, укажите имя пользователя для исключения.")
            return

        kicked_player = session.query(Player).filter_by(username=username).first()
        if not kicked_player or kicked_player not in room.players:
            bot.send_message(message.chat.id, "❗ Игрок не найден в комнате.")
            return

        room.players.remove(kicked_player)
        kicked_player.current_room_id = None

        # Удаляем характеристики исключенного игрока
        characteristics = session.query(Characteristic).filter_by(player_id=kicked_player.id).first()
        if characteristics:
            session.delete(characteristics)

        session.commit()

        bot.send_message(message.chat.id, f"🚫 Игрок <b>{username}</b> был исключен из комнаты.", parse_mode='HTML')
        bot.send_message(kicked_player.telegram_id, "❗ Вы были исключены из комнаты.")
    except Exception as e:
        session.rollback()
        bot.send_message(message.chat.id, "Произошла ошибка при исключении игрока.")
        logging.error(f"Ошибка в handle_kick_player: {e}")
    finally:
        session.close()

def handle_stop_game(bot, message):
    logging.info(f"Пользователь {message.from_user.id} вызвал команду /stop_game")
    session = Session()
    try:
        telegram_id = message.from_user.id
        player = session.query(Player).filter_by(telegram_id=telegram_id).first()

        if not player:
            bot.send_message(message.chat.id, "❗ Вы не зарегистрированы. Используйте /start для начала.")
            return

        room = session.query(Room).filter_by(id=player.current_room_id).first()
        if not room or room.host_id != player.id:
            bot.send_message(message.chat.id, "❗ Вы не являетесь хостом комнаты.")
            return

        room.is_active = False
        session.commit()

        bot.send_message(message.chat.id, "⛔ Игра завершена.")

        # Обновляем информацию для всех игроков в комнате
        for p in room.players:
            try:
                p.current_room_id = None

                # Удаляем характеристики игрока
                characteristics = session.query(Characteristic).filter_by(player_id=p.id).first()
                if characteristics:
                    session.delete(characteristics)

                session.commit()
                bot.send_message(p.telegram_id, "❗ Игра была завершена хостом. Ваши характеристики сброшены.")
            except Exception as e:
                session.rollback()
                logging.error(f"Ошибка при отправке сообщения пользователю {p.telegram_id}: {e}")
                # Отправляем хосту информацию о проблеме
                bot.send_message(message.chat.id, f"❗ Не удалось отправить сообщение пользователю {p.username}.")

    except Exception as e:
        session.rollback()
        bot.send_message(message.chat.id, "❗ Произошла ошибка при завершении игры.")
        logging.error(f"Ошибка в handle_stop_game: {e}")
    finally:
        session.close()


def handle_start_discussion(bot, message):
    logging.info(f"Пользователь {message.from_user.id} вызвал команду /start_discussion")
    session = Session()
    try:
        telegram_id = message.from_user.id
        player = session.query(Player).filter_by(telegram_id=telegram_id).first()

        if not player:
            bot.send_message(message.chat.id, "❗ Вы не зарегистрированы. Используйте /start для начала.")
            return

        room = session.query(Room).filter_by(id=player.current_room_id).first()
        if not room or room.host_id != player.id:
            bot.send_message(message.chat.id, "❗ Вы не являетесь хостом комнаты.")
            return

        room.is_voting = False
        session.commit()

        for p in room.players:
            bot.send_message(p.telegram_id, "💬 Обсуждение началось! Вы можете обсуждать свои характеристики.")
    except Exception as e:
        session.rollback()
        bot.send_message(message.chat.id, "Произошла ошибка при начале обсуждения.")
        logging.error(f"Ошибка в handle_start_discussion: {e}")
    finally:
        session.close()

def handle_end_discussion(bot, message):
    logging.info(f"Пользователь {message.from_user.id} вызвал команду /end_discussion")
    session = Session()
    try:
        telegram_id = message.from_user.id
        player = session.query(Player).filter_by(telegram_id=telegram_id).first()

        if not player:
            bot.send_message(message.chat.id, "❗ Вы не зарегистрированы. Используйте /start для начала.")
            return

        room = session.query(Room).filter_by(id=player.current_room_id).first()
        if not room or room.host_id != player.id:
            bot.send_message(message.chat.id, "❗ Вы не являетесь хостом комнаты.")
            return

        room.is_voting = True
        session.commit()

        for p in room.players:
            bot.send_message(p.telegram_id, "🗳️ Обсуждение завершено! Начинается голосование.")
            handle_vote_command(bot, p.telegram_id)
    except Exception as e:
        session.rollback()
        bot.send_message(message.chat.id, "Произошла ошибка при завершении обсуждения.")
        logging.error(f"Ошибка в handle_end_discussion: {e}")
    finally:
        session.close()

def handle_vote_command(bot, chat_id):
    session = Session()
    try:
        voter = session.query(Player).filter_by(telegram_id=chat_id).first()
        if not voter:
            bot.send_message(chat_id, "❗ Вы не зарегистрированы. Используйте /start для начала.")
            return

        room = session.query(Room).filter_by(id=voter.current_room_id).first()
        if not room:
            bot.send_message(chat_id, "❗ Вы не находитесь в комнате.")
            return

        if not room.is_voting:
            bot.send_message(chat_id, "❗ Сейчас не время для голосования.")
            return

        existing_vote = session.query(Vote).filter_by(room_id=room.id, voter_id=voter.id).first()
        if existing_vote:
            bot.send_message(chat_id, "❗ Вы уже проголосовали.")
            return

        players_in_room = [p for p in room.players if p.telegram_id != voter.telegram_id]
        markup = create_voting_buttons(players_in_room)
        bot.send_message(chat_id, "🗳️ Выберите игрока для исключения:", reply_markup=markup)
    except Exception as e:
        bot.send_message(chat_id, "Произошла ошибка при начале голосования.")
        logging.error(f"Ошибка в handle_vote_command: {e}")
    finally:
        session.close()

def handle_vote_callback(bot, call):
    session = Session()
    try:
        voter_id = call.from_user.id
        voted_player_telegram_id = int(call.data.split('_')[1])

        voter = session.query(Player).filter_by(telegram_id=voter_id).first()
        if not voter:
            bot.answer_callback_query(call.id, "❗ Вы не зарегистрированы.")
            return

        room = session.query(Room).filter_by(id=voter.current_room_id).first()
        if not room or not room.is_voting:
            bot.answer_callback_query(call.id, "❗ Сейчас не время для голосования.")
            return

        existing_vote = session.query(Vote).filter_by(room_id=room.id, voter_id=voter.id).first()
        if existing_vote:
            bot.answer_callback_query(call.id, "❗ Вы уже проголосовали!")
            return

        voted_player = session.query(Player).filter_by(telegram_id=voted_player_telegram_id).first()
        if not voted_player:
            bot.answer_callback_query(call.id, "❗ Выбранный игрок не найден.")
            return

        vote = Vote(room_id=room.id, voter_id=voter.id, voted_player_id=voted_player.id)
        session.add(vote)
        session.commit()

        bot.answer_callback_query(call.id, "✅ Ваш голос учтен!")

        total_votes = session.query(Vote).filter_by(room_id=room.id).count()
        total_players = len(room.players)

        if total_votes == total_players:
            handle_vote_results(bot, room)
    except Exception as e:
        session.rollback()
        bot.answer_callback_query(call.id, "❗ Произошла ошибка при голосовании.")
        logging.error(f"Ошибка в handle_vote_callback: {e}")
    finally:
        session.close()

# handlers/admin_handlers.py



def handle_vote_results(bot, room):
    session = Session()
    try:
        votes = session.query(Vote).filter_by(room_id=room.id).all()
        vote_counts = {}
        for vote in votes:
            vote_counts[vote.voted_player_id] = vote_counts.get(vote.voted_player_id, 0) + 1

        max_votes = max(vote_counts.values())
        players_with_max_votes = [pid for pid, count in vote_counts.items() if count == max_votes]

        # Получаем объект хоста
        host = session.query(Player).filter_by(id=room.host_id).first()

        if len(players_with_max_votes) > 1:
            if host:
                bot.send_message(host.telegram_id, "⚖️ Ничья при голосовании. Необходимо переголосовать.")
            session.query(Vote).filter_by(room_id=room.id).delete()
            session.commit()
            for player in room.players:
                bot.send_message(player.telegram_id, "🗳️ Переголосование началось!")
                handle_vote_command(bot, player.telegram_id)
            return

        excluded_player_id = players_with_max_votes[0]
        excluded_player = session.query(Player).filter_by(id=excluded_player_id).first()

        if excluded_player:
            # Ищем объект игрока в списке room.players
            player_in_room = next((p for p in room.players if p.id == excluded_player.id), None)
            if player_in_room:
                room.players.remove(player_in_room)
                excluded_player.current_room_id = None

                # Удаляем характеристики исключенного игрока
                characteristics = session.query(Characteristic).filter_by(player_id=excluded_player.id).first()
                if characteristics:
                    session.delete(characteristics)

                session.commit()

                for player in room.players:
                    bot.send_message(player.telegram_id, f"🚫 Игрок <b>{excluded_player.username}</b> был исключен из бункера.", parse_mode='HTML')
                bot.send_message(excluded_player.telegram_id, "❗ Вы были исключены из бункера.")

                # Отправляем характеристики исключенного игрока остальным
                characteristics_text = f"""
<b>Характеристики исключенного игрока {excluded_player.username}:</b>
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
                for player in room.players:
                    bot.send_message(player.telegram_id, characteristics_text, parse_mode='HTML')

                # Удаляем все голоса
                session.query(Vote).filter_by(room_id=room.id).delete()
                session.commit()

                if len(room.players) <= room.survivors:
                    end_game(bot, room)
                else:
                    trigger_random_event(bot, room)
                    if host:
                        bot.send_message(host.telegram_id, "💬 Используйте /start_discussion для начала следующего раунда обсуждения.")
            else:
                logging.error(f"Игрок с id {excluded_player.id} не найден в комнате {room.id}")
                bot.send_message(room.host_id, f"❗ Игрок с id {excluded_player.id} не найден в комнате.")
        else:
            logging.error(f"Игрок с id {excluded_player_id} не найден в базе данных.")
            bot.send_message(room.host_id, f"❗ Игрок с id {excluded_player_id} не найден в базе данных.")
    except Exception as e:
        session.rollback()
        if host:
            bot.send_message(host.telegram_id, "❗ Произошла ошибка при обработке результатов голосования.")
        logging.error(f"Ошибка в handle_vote_results: {e}")
    finally:
        session.close()


def end_game(bot, room):
    session = Session()
    try:
        survivors_needed = room.survivors
        # Получаем список выживших игроков (остальные - проигравшие)
        survivors = room.players.copy()  # Копируем список, чтобы избежать изменений во время итерации
        winner_usernames = [player.username for player in survivors]
        winners_text = "🎉 <b>Игра завершена!</b>\n\n<b>Выжившие игроки:</b>\n" + "\n".join(winner_usernames)
        
        for player in survivors:
            bot.send_message(player.telegram_id, winners_text, parse_mode='HTML')
            player.wins += 1  # Увеличиваем количество побед
            player.current_room_id = None

            # Удаляем характеристики игрока
            characteristics = session.query(Characteristic).filter_by(player_id=player.id).first()
            if characteristics:
                session.delete(characteristics)

            session.commit()

            # Проверяем достижения
            check_and_award_achievements(bot, player)

        # Получаем список проигравших игроков
        excluded_players = session.query(Player).filter(Player.current_room_id == room.id).all()
        losers_usernames = [player.username for player in excluded_players]
        losers_text = "<b>Пораженные игроки:</b>\n" + "\n".join(losers_usernames) if losers_usernames else ""
        
        for player in excluded_players:
            player.losses += 1  # Увеличиваем количество поражений
            player.current_room_id = None

            # Удаляем характеристики игрока
            characteristics = session.query(Characteristic).filter_by(player_id=player.id).first()
            if characteristics:
                session.delete(characteristics)

            session.commit()

            # Отправляем сообщение проигравшему (если необходимо)
            bot.send_message(player.telegram_id, "❗ Вы проиграли в игре.", parse_mode='HTML')

        room.is_active = False
        session.commit()

        # Получаем случайную концовку и отправляем игрокам
        ending = get_random_ending()
        for player in survivors:
            bot.send_message(player.telegram_id, f"🏁 <b>Концовка игры:</b>\n{ending}", parse_mode='HTML')
    except Exception as e:
        session.rollback()
        host = session.query(Player).filter_by(id=room.host_id).first()
        if host:
            bot.send_message(host.telegram_id, "❗ Произошла ошибка при завершении игры.")
        logging.error(f"Ошибка в end_game: {e}")
    finally:
        session.close()

def handle_timer(bot, message):
    logging.info(f"Пользователь {message.from_user.id} вызвал команду /timer")
    session = Session()
    try:
        telegram_id = message.from_user.id
        player = session.query(Player).filter_by(telegram_id=telegram_id).first()

        if not player:
            bot.send_message(message.chat.id, "❗ Вы не зарегистрированы. Используйте /start для начала.")
            return

        room = session.query(Room).filter_by(id=player.current_room_id).first()
        if not room or room.host_id != player.id:
            bot.send_message(message.chat.id, "❗ Вы не являетесь хостом комнаты.")
            return

        # Парсим аргументы команды /timer, ожидается количество минут
        try:
            args = message.text.split()
            if len(args) != 2:
                bot.send_message(message.chat.id, "❗ Пожалуйста, укажите время таймера в минутах.\nПример: /timer 10")
                return
            timer_minutes = int(args[1])
            if timer_minutes <= 0:
                bot.send_message(message.chat.id, "❗ Время должно быть положительным числом.")
                return
        except ValueError:
            bot.send_message(message.chat.id, "❗ Некорректный формат времени. Укажите число минут.\nПример: /timer 10")
            return

        # Уведомляем всех игроков о запуске таймера
        for p in room.players:
            try:
                bot.send_message(p.telegram_id, f"⏰ Таймер на {timer_minutes} минут запущен хостом.")
            except ApiException as api_e:
                logging.error(f"API ошибка при отправке сообщению пользователю {p.telegram_id}: {api_e}")
                bot.send_message(message.chat.id, f"❗ Не удалось отправить сообщение пользователю {p.username}.")
            except Exception as e:
                logging.error(f"Неизвестная ошибка при отправке сообщению пользователю {p.telegram_id}: {e}")
                bot.send_message(message.chat.id, f"❗ Не удалось отправить сообщение пользователю {p.username}.")

        # Запускаем отдельный поток для отсчёта времени
        timer_thread = threading.Thread(target=timer_countdown, args=(bot, room.id, timer_minutes))
        timer_thread.start()

        bot.send_message(message.chat.id, f"⏰ Таймер на {timer_minutes} минут запущен.")
    except Exception as e:
        session.rollback()
        bot.send_message(message.chat.id, "❗ Произошла ошибка при запуске таймера.")
        logging.error(f"Ошибка в handle_timer: {e}")
    finally:
        session.close()

def timer_countdown(bot, room_id, minutes):
    try:
        time.sleep(minutes * 60)  # Ждём указанное количество минут

        session = Session()
        room = session.query(Room).filter_by(id=room_id).first()
        if not room or not room.is_active:
            session.close()
            return

        # Уведомляем всех игроков о завершении таймера
        for p in room.players:
            try:
                bot.send_message(p.telegram_id, f"⏰ Таймер на {minutes} минут завершён.")
            except ApiException as api_e:
                logging.error(f"API ошибка при отправке сообщению пользователю {p.telegram_id}: {api_e}")
            except Exception as e:
                logging.error(f"Неизвестная ошибка при отправке сообщению пользователю {p.telegram_id}: {e}")

        # Можно добавить автоматическое завершение обсуждения или начать голосование
        # Например, автоматическое завершение обсуждения:
        room.is_voting = True
        session.commit()

        for p in room.players:
            try:
                bot.send_message(p.telegram_id, "🗳️ Время обсуждения истекло. Начинается голосование.", parse_mode='HTML')
            except ApiException as api_e:
                logging.error(f"API ошибка при отправке сообщению пользователю {p.telegram_id}: {api_e}")
            except Exception as e:
                logging.error(f"Неизвестная ошибка при отправке сообщению пользователю {p.telegram_id}: {e}")

        # Запускаем процесс голосования
        from handlers.admin_handlers import handle_vote_command  # Импорт внутри функции, чтобы избежать циклических импортов
        for p in room.players:
            handle_vote_command(bot, p.telegram_id)

    except Exception as e:
        logging.error(f"Ошибка в timer_countdown: {e}")
         
def trigger_random_event(bot, room):
    event = get_random_event()
    for player in room.players:
        bot.send_message(player.telegram_id, f"🔔 <b>Случайное событие:</b>\n{event}", parse_mode='HTML')
