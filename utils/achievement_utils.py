# utils/achievement_utils.py

from database import Session
from models import Achievement, PlayerAchievement
import logging

def check_and_award_achievements(bot, player):
    session = Session()
    try:
        # Пример: достижение за первую победу
        if player.wins == 1:
            achievement = session.query(Achievement).filter_by(name='Первая победа').first()
            if achievement:
                existing = session.query(PlayerAchievement).filter_by(player_id=player.id, achievement_id=achievement.id).first()
                if not existing:
                    player_achievement = PlayerAchievement(player_id=player.id, achievement_id=achievement.id)
                    session.add(player_achievement)
                    session.commit()
                    bot.send_message(player.telegram_id, f"🏅 Вы получили достижение: {achievement.name}!")
        
        # Добавьте дополнительные проверки для других достижений
        # Пример: достижение за участие в 5 играх
        if player.wins + player.losses == 5:
            achievement = session.query(Achievement).filter_by(name='Участник').first()
            if achievement:
                existing = session.query(PlayerAchievement).filter_by(player_id=player.id, achievement_id=achievement.id).first()
                if not existing:
                    player_achievement = PlayerAchievement(player_id=player.id, achievement_id=achievement.id)
                    session.add(player_achievement)
                    session.commit()
                    bot.send_message(player.telegram_id, f"🎖️ Вы получили достижение: {achievement.name}!")
        
        # Пример: достижение за победу в 10 играх
        if player.wins == 10:
            achievement = session.query(Achievement).filter_by(name='Победитель').first()
            if achievement:
                existing = session.query(PlayerAchievement).filter_by(player_id=player.id, achievement_id=achievement.id).first()
                if not existing:
                    player_achievement = PlayerAchievement(player_id=player.id, achievement_id=achievement.id)
                    session.add(player_achievement)
                    session.commit()
                    bot.send_message(player.telegram_id, f"🏆 Вы получили достижение: {achievement.name}!")
    except Exception as e:
        logging.error(f"Ошибка в check_and_award_achievements: {e}")
    finally:
        session.close()
