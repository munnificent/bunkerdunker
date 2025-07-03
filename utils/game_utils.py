# utils/game_utils.py

import random
import string
import logging
from typing import Dict, Any, List, Type
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from models import (
    Player, Characteristic, Location, Room,
    Profession, Biology, Health, Hobby, Luggage, Fact,
    Phobia, Talent, SocialStatus, Base
)

# --- Константы ---

RANDOM_EVENTS: List[str] = [
    "🔌 Отключение электроэнергии в бункере! Нужно найти способ восстановить питание.",
    "💧 Запасы воды начинают истощаться. Требуется рационализировать потребление.",
    "📡 Обнаружен слабый сигнал извне. Попытайтесь установить связь.",
    "🛠 Неисправность в системе жизнеобеспечения. Нужен специалист для ремонта.",
    "🌡 Температура в бункере резко упала. Необходимо согреться и найти причину.",
    "🕳 Обнаружен скрытый проход в стене. Решите, исследовать ли его.",
    "🍽 Запасы пищи испортились. Нужно найти альтернативные источники питания.",
    "📦 Найден ящик с неизвестным содержимым. Откроете ли вы его?",
    "🐍 В бункере обнаружены змеи! Нужно их обезвредить.",
    "🔒 Сработала система безопасности, блокируя доступ к важным ресурсам.",
    "📻 Поймали странное радиосообщение. Расшифруйте его содержание.",
    "🌱 В гидропонной ферме выросли неизвестные растения.",
    "🧟 Появились признаки активности снаружи бункера. Выясните, что происходит.",
    "🗺 Обнаружена старая карта с отмеченным тайником. Отправитесь ли вы за ним?",
]

RANDOM_ENDINGS: List[str] = [
    "🌅 Выжившие успешно обустроили новое общество и восстановили цивилизацию.",
    "🛰️ Выжившие обнаружили сигналы с другого мира и отправились в космос на поиски новой планеты.",
    "🌋 Бункер оказался на грани вулканического извержения, и выжившие чудом спаслись.",
    "👽 Выжившие столкнулись с неизвестной формой жизни, и их дальнейшая судьба неизвестна.",
    "🌊 Поднявшийся уровень океана затопил бункер, но выжившие успели покинуть его на подводной лодке.",
    "🧬 Выжившие нашли способ обратить катастрофу и вернуть мир к прежней жизни."
]

# --- Функции ---

def generate_unique_room_code(session: Session, max_attempts: int = 10) -> str:
    """
    Генерирует уникальный 6-значный код для комнаты.
    
    Args:
        session: Активная сессия SQLAlchemy.
        max_attempts: Максимальное количество попыток генерации.

    Returns:
        Уникальный код комнаты.
    
    Raises:
        RuntimeError: Если не удалось сгенерировать уникальный код за max_attempts.
    """
    for _ in range(max_attempts):
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        existing_room = session.query(Room).filter_by(code=code).first()
        if not existing_room:
            return code
    raise RuntimeError("Не удалось сгенерировать уникальный код комнаты. Попробуйте снова.")

def _get_random_record(session: Session, model: Type[Base]) -> Any:
    """Вспомогательная функция для получения случайной записи из таблицы-справочника."""
    return session.query(model).order_by(func.random()).first()

def assign_new_characteristics_to_player(session: Session, player: Player) -> Characteristic:
    """
    Генерирует и присваивает игроку новые характеристики персонажа.
    Оптимизировано для работы в рамках одной сессии.

    Args:
        session: Активная сессия SQLAlchemy.
        player: Объект игрока, которому присваиваются характеристики.

    Returns:
        Объект Characteristic с новыми данными.
    """
    # 1. Получаем все необходимые случайные данные за одну сессию
    profession_obj = _get_random_record(session, Profession)
    biology_obj = _get_random_record(session, Biology)
    health_obj = _get_random_record(session, Health)
    hobby_obj = _get_random_record(session, Hobby)
    luggage_obj = _get_random_record(session, Luggage)
    fact_obj = _get_random_record(session, Fact)
    phobia_obj = _get_random_record(session, Phobia)
    talent_obj = _get_random_record(session, Talent)
    social_status_obj = _get_random_record(session, SocialStatus)

    # 2. Формируем словарь с данными, предусматривая случаи, если какая-то таблица пуста
    char_data = {
        'profession': profession_obj.name if profession_obj else "Безработный",
        'biology': f"{biology_obj.gender}, {biology_obj.age} лет, {biology_obj.body_features}" if biology_obj else "Неизвестно",
        'health': health_obj.condition if health_obj else "Здоров",
        'hobby': hobby_obj.hobby if hobby_obj else "Нет хобби",
        'luggage': luggage_obj.item if luggage_obj else "Пусто",
        'facts': fact_obj.fact if fact_obj else "Нет фактов",
        'phobia': phobia_obj.phobia if phobia_obj else "Нет фобий",
        'talent': talent_obj.talent if talent_obj else "Нет талантов",
        'social_status': social_status_obj.status if social_status_obj else "Средний класс",
    }

    # 3. Проверяем, есть ли у игрока уже характеристики, и обновляем или создаем их
    characteristics = session.query(Characteristic).filter_by(player_id=player.id).first()
    
    if characteristics:
        # Обновляем существующие
        for key, value in char_data.items():
            setattr(characteristics, key, value)
        logging.info(f"Обновлены характеристики для игрока {player.username} ({player.id}).")
    else:
        # Создаем новые
        characteristics = Characteristic(player_id=player.id, **char_data)
        session.add(characteristics)
        logging.info(f"Созданы новые характеристики для игрока {player.username} ({player.id}).")
        
    # Коммит будет выполнен в вызывающей функции (в хендлере)
    return characteristics

def get_random_location(session: Session) -> Location | None:
    """Возвращает случайную локацию (катастрофу) из базы данных."""
    return _get_random_record(session, Location)

def get_random_event() -> str:
    """Возвращает случайное игровое событие из предопределенного списка."""
    return random.choice(RANDOM_EVENTS)

def get_random_ending() -> str:
    """Возвращает случайную концовку игры из предопределенного списка."""
    return random.choice(RANDOM_ENDINGS)