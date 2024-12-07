# utils/game_utils.py

import random
from database import Session
from models import (
    Player, Characteristic, Location, Room,
    Profession, Biology, Health, Hobby, Luggage, Fact,
    Phobia, Talent, SocialStatus, Achievement, PlayerAchievement
)
from sqlalchemy.sql import func

def generate_unique_room_code():
    import string
    session = Session()
    existing_codes = {code[0] for code in session.query(Room.code).all()}
    while True:
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        if code not in existing_codes:
            session.close()
            return code

def generate_characteristics():
    session = Session()
    # Профессия
    profession_obj = session.query(Profession).order_by(func.random()).first()
    profession = profession_obj.name if profession_obj else "Безработный"

    # Биология
    biology_obj = session.query(Biology).order_by(func.random()).first()
    if biology_obj:
        biology = f"{biology_obj.gender}, {biology_obj.age} лет, {biology_obj.body_features}"
    else:
        biology = "Неизвестно"

    # Здоровье
    health_obj = session.query(Health).order_by(func.random()).first()
    health = health_obj.condition if health_obj else "Здоров"

    # Хобби
    hobby_obj = session.query(Hobby).order_by(func.random()).first()
    hobby = hobby_obj.hobby if hobby_obj else "Нет хобби"

    # Багаж
    luggage_obj = session.query(Luggage).order_by(func.random()).first()
    luggage = luggage_obj.item if luggage_obj else "Пусто"

    # Факт
    fact_obj = session.query(Fact).order_by(func.random()).first()
    fact = fact_obj.fact if fact_obj else "Нет фактов"

    # Фобия
    phobia_obj = session.query(Phobia).order_by(func.random()).first()
    phobia = phobia_obj.phobia if phobia_obj else "Нет фобий"

    # Талант
    talent_obj = session.query(Talent).order_by(func.random()).first()
    talent = talent_obj.talent if talent_obj else "Нет талантов"

    # Социальный статус
    social_status_obj = session.query(SocialStatus).order_by(func.random()).first()
    social_status = social_status_obj.status if social_status_obj else "Средний класс"

    session.close()

    return {
        'profession': profession,
        'biology': biology,
        'health': health,
        'hobby': hobby,
        'luggage': luggage,
        'facts': fact,
        'phobia': phobia,
        'talent': talent,
        'social_status': social_status
    }

def assign_characteristics_to_player(player):
    session = Session()
    try:
        # Проверяем, есть ли у игрока уже характеристики
        characteristics = session.query(Characteristic).filter_by(player_id=player.id).first()
        
        # Генерируем новые характеристики
        char_data = generate_characteristics()
        
        if characteristics:
            # Обновляем существующие характеристики
            characteristics.profession = char_data['profession']
            characteristics.biology = char_data['biology']
            characteristics.health = char_data['health']
            characteristics.hobby = char_data['hobby']
            characteristics.luggage = char_data['luggage']
            characteristics.facts = char_data['facts']
            characteristics.phobia = char_data['phobia']
            characteristics.talent = char_data['talent']
            characteristics.social_status = char_data['social_status']
        else:
            # Создаем новые характеристики
            characteristics = Characteristic(
                player_id=player.id,
                profession=char_data['profession'],
                biology=char_data['biology'],
                health=char_data['health'],
                hobby=char_data['hobby'],
                luggage=char_data['luggage'],
                facts=char_data['facts'],
                phobia=char_data['phobia'],
                talent=char_data['talent'],
                social_status=char_data['social_status']
            )
            session.add(characteristics)
        
        session.commit()
        return characteristics
    except Exception as e:
        session.rollback()
        print(f"Ошибка в assign_characteristics_to_player: {e}")
    finally:
        session.close()

def generate_location():
    session = Session()
    location = session.query(Location).order_by(func.random()).first()
    session.close()
    return location

def get_random_event():
    events = [
    "🔌 Отключение электроэнергии в бункере! Нужно найти способ восстановить питание.",
    "💧 Запасы воды начинают истощаться. Требуется рационализировать потребление.",
    "📡 Обнаружен слабый сигнал извне. Попытайтесь установить связь.",
    "🛠 Неисправность в системе жизнеобеспечения. Нужен специалист для ремонта.",
    "🌡 Температура в бункере резко упала. Необходимо согреться и найти причину.",
    "🕳 Обнаружен скрытый проход в стене. Решите, исследовать ли его.",
    "🍽 Запасы пищи испортились. Нужно найти альтернативные источники питания.",
    "📦 Найден ящик с неизвестным содержимым. Откроете ли вы его?",
    "🚪 Дверь в один из отсеков заклинило. Нужно найти способ ее открыть.",
    "🐍 В бункере обнаружены змеи! Нужно их обезвредить.",
    "💡 Система освещения мерцает. Необходимо проверить электропроводку.",
    "🔒 Сработала система безопасности, блокируя доступ к важным ресурсам.",
    "🧯 Пожарная тревога сработала без видимой причины. Проверить систему.",
    "📻 Поймали странное радиосообщение. Расшифруйте его содержание.",
    "🌱 В гидропонной ферме выросли неизвестные растения.",
    "🧟 Появились признаки активности снаружи бункера. Выясните, что происходит.",
    "🚰 Вода стала мутной. Проверьте систему фильтрации.",
    "🔭 На горизонте виден странный свет. Решите, стоит ли его исследовать.",
    "🕹 Неисправность в системе управления. Бункер начинает жить своей жизнью.",
    "🗺 Обнаружена старая карта с отмеченным тайником. Отправитесь ли вы за ним?",
    "🐜 Нашествие насекомых в одном из отсеков. Необходимо принять меры.",
    "⏳ Время на часах бункера сбилось. Нужно определить точное время.",
    "🌪 Снаружи бушует шторм. Решите, как защитить бункер от повреждений.",
    "🎭 Один из членов команды ведет себя странно. Проведите беседу.",
    "🔋 Запасные генераторы вышли из строя. Необходимо их починить.",
    "🛰 Обнаружен спутник на орбите. Попробуйте установить с ним связь.",
    "❄️ Система отопления перегрелась. Требуется немедленный ремонт.",
    "🐾 Найдены следы неизвестного существа внутри бункера.",
    "📀 Найден диск с зашифрованными данными. Расшифруйте их.",
    "🛒 Появилась возможность совершить вылазку за припасами. Решите, кто пойдет.",
    "🚀 Получен сигнал о возможной эвакуации. Подготовьтесь к отбытию.",
    "⚙️ Один из механизмов бункера начал работать неправильно. Определите причину.",
    "🧪 В лаборатории произошла утечка химикатов. Примите меры безопасности.",
    "🎙 Обнаружен старый микрофон. Возможно, можно передать сообщение наружу.",
    "📢 В бункере раздается неизвестный голос. Найдите источник.",
    "🔑 Потерян ключ от важного отсека. Нужно его найти.",
    "💤 У всех участников начали повторяться одни и те же сны. Что бы это значило?",
    "🛎 Неожиданно зазвенел звонок у входной двери. Кто мог там быть?",
    "🚧 Обрушение в одном из туннелей. Необходимо расчистить завалы.",
    "🖥 Сбой в компьютерной системе. Возможно, это кибератака.",
    "🌋 Сейсмическая активность увеличивается. Подготовьтесь к возможным последствиям.",
    "📈 Датчики показывают повышение радиации. Примите меры предосторожности.",
    "🧩 Найдены части головоломки. Возможно, они что-то открывают.",
    "🎒 Пропали личные вещи некоторых членов команды. Проведите расследование.",
    "📚 В архиве обнаружены документы с секретной информацией.",
    "🚿 Система водоснабжения вышла из строя. Требуется срочный ремонт.",
    "🔊 Услышаны странные шумы из вентиляции. Исследуйте их источник.",
    "🕰 Время внутри бункера идет быстрее, чем снаружи. Разберитесь в причине.",
    "🗞 Появилась свежая газета с сегодняшней датой. Как это возможно?",
]
    event = random.choice(events)
    return event

def get_random_ending():
    endings = [
        "🌅 Выжившие успешно обустроили новое общество и восстановили цивилизацию.",
        "🛰️ Выжившие обнаружили сигналы с другого мира и отправились в космос на поиски новой планеты.",
        "🌋 Бункер оказался на грани вулканического извержения, и выжившие чудом спаслись.",
        "👽 Выжившие столкнулись с неизвестной формой жизни, и их дальнейшая судьба неизвестна.",
        "🌊 Поднявшийся уровень океана затопил бункер, но выжившие успели покинуть его на подводной лодке.",
        "🧬 Выжившие нашли способ обратить катастрофу и вернуть мир к прежней жизни."
    ]
    ending = random.choice(endings)
    return ending
