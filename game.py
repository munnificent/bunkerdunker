import sqlite3

# Подключение к базе данных (если базы нет, она будет создана)
conn = sqlite3.connect('bunker_game.db')
cursor = conn.cursor()

# Создание таблиц
def create_tables():
    # Таблица профессий
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS professions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')

    # Таблица биологии
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS biology (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            gender TEXT NOT NULL,
            age INTEGER NOT NULL,
            body_features TEXT
        )
    ''')

    # Таблица здоровья
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS health (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            condition TEXT NOT NULL
        )
    ''')

    # Таблица хобби
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS hobbies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hobby TEXT NOT NULL
        )
    ''')

    # Таблица багажа
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS luggage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item TEXT NOT NULL
        )
    ''')

    # Таблица фактов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS facts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fact TEXT NOT NULL
        )
    ''')

    # Таблица локаций
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS locations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            survival_conditions TEXT NOT NULL
        )
    ''')

    conn.commit()

# Заполнение таблиц данными
def populate_tables():
    # Примеры данных (их можно расширить или заменить)
    professions = [
        ('Врач',),
        ('Инженер',),
        ('Учитель',),
        ('Фермер',),
        ('Повар',),
        ('Военный',),
        ('Учёный',),
        ('Художник',),
        ('Музыкант',),
        ('Программист',)
    ]

    biology = [
        ('Мужчина', 25, 'Рост 180 см, карие глаза'),
        ('Женщина', 30, 'Рост 165 см, блондинка'),
        ('Мужчина', 40, 'Рост 170 см, очки'),
        ('Женщина', 22, 'Рост 160 см, спортсменка'),
        ('Мужчина', 35, 'Рост 175 см, борода'),
        ('Женщина', 28, 'Рост 168 см, зелёные глаза'),
        ('Мужчина', 50, 'Рост 182 см, седые волосы'),
        ('Женщина', 45, 'Рост 158 см, веснушки'),
        ('Мужчина', 60, 'Рост 165 см, лысый'),
        ('Женщина', 33, 'Рост 170 см, татуировки')
    ]

    health = [
        ('Абсолютно здоров',),
        ('Аллергия на орехи',),
        ('Диабет',),
        ('Проблемы со зрением',),
        ('Беременность',),
        ('Сердечные заболевания',),
        ('Астма',),
        ('Хроническая усталость',),
        ('Инвалидность (нет руки)',),
        ('Повышенное давление',)
    ]

    hobbies = [
        ('Чтение',),
        ('Плавание',),
        ('Рыбалка',),
        ('Готовка',),
        ('Игра на гитаре',),
        ('Рисование',),
        ('Путешествия',),
        ('Садоводство',),
        ('Йога',),
        ('Шахматы',)
    ]

    luggage = [
        ('Нож',),
        ('Аптечка',),
        ('Семена растений',),
        ('Спальный мешок',),
        ('Топор',),
        ('Рация',),
        ('Запас еды на 3 дня',),
        ('Карта местности',),
        ('Фонарик',),
        ('Гитара',)
    ]

    facts = [
        ('Спас жизнь человеку',),
        ('Знает 3 иностранных языка',),
        ('Имеет криминальное прошлое',),
        ('Участник Олимпийских игр',),
        ('Имеет IQ выше 140',),
        ('Был в космосе',),
        ('Может выживать в дикой природе',),
        ('Является миллиардером',),
        ('Не умеет плавать',),
        ('Бесстрашный альпинист',)
    ]

    locations = [
        ('Бункер в горах', 'Нужны теплые вещи и навыки альпинизма'),
        ('Подземный бункер в пустыне', 'Нужна вода и защита от жары'),
        ('Бункер на острове', 'Необходимы навыки рыбалки и мореплавания'),
        ('Бункер в лесу', 'Полезны знания о растениях и животных'),
        ('Городской бункер', 'Нужны навыки выживания в городе')
    ]

    # Вставка данных в таблицы
    cursor.executemany('INSERT INTO professions (name) VALUES (?)', professions)
    cursor.executemany('INSERT INTO biology (gender, age, body_features) VALUES (?, ?, ?)', biology)
    cursor.executemany('INSERT INTO health (condition) VALUES (?)', health)
    cursor.executemany('INSERT INTO hobbies (hobby) VALUES (?)', hobbies)
    cursor.executemany('INSERT INTO luggage (item) VALUES (?)', luggage)
    cursor.executemany('INSERT INTO facts (fact) VALUES (?)', facts)
    cursor.executemany('INSERT INTO locations (description, survival_conditions) VALUES (?, ?)', locations)

    conn.commit()

# Основная функция
def main():
    create_tables()
    populate_tables()
    print("База данных успешно создана и заполнена.")

if __name__ == '__main__':
    main()

    # Закрытие соединения с базой данных
    conn.close()
