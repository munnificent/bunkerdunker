# populate_db.py

from database import engine, Session
from models import (
    Base, Profession, Biology, Health, Hobby, Luggage, Fact,
    Location, Phobia, Talent, SocialStatus, Achievement
)

def create_tables():
    Base.metadata.create_all(engine)
    print("Все таблицы успешно созданы.")

def populate_professions():
    session = Session()
    professions = [
        Profession(name='Инженер'),
        Profession(name='Врач'),
        Profession(name='Учитель'),
        Profession(name='Фермер'),
        Profession(name='Повар'),
        Profession(name='Пилот'),
        Profession(name='Клоун'),
        Profession(name='Механик'),
        Profession(name='Военный'),
        Profession(name='Дворник'),
        Profession(name='Биолог'),
        Profession(name='Охотник на демонов'),
        Profession(name='Химик'),
        Profession(name='Архитектор'),
        Profession(name='Писатель'),
        Profession(name='Программист'),
        Profession(name='Юрист'),
        Profession(name='Музыкант'),
        Profession(name='Астроном'),
        Profession(name='Журналист'),
        Profession(name='Психолог'),
        Profession(name='Пожарный'),
        Profession(name='Полицейский'),
        Profession(name='Лаборант'),
        Profession(name='Геолог'),
        Profession(name='Фотограф'),
        Profession(name='Актёр'),
        Profession(name='Дизайнер'),
        Profession(name='Экономист'),
        Profession(name='Садовник'),
        Profession(name='Сантехник'),
        Profession(name='Электрик'),
        Profession(name='Моряк'),
        Profession(name='Тренер'),
        Profession(name='Ветеринар'),
        Profession(name='Пекарь'),
        Profession(name='Водитель'),
        Profession(name='Менеджер'),
        Profession(name='Строитель'),
        Profession(name='Массажист'),
        Profession(name='Кузнец'),
        Profession(name='Археолог'),
        Profession(name='Парикмахер'),
        Profession(name='Лесоруб'),
        Profession(name='Слесарь'),
        Profession(name='Кондитер'),
        Profession(name='Метеоролог'),
        Profession(name='Бортпроводник'),
        Profession(name='Дирижёр'),
        Profession(name='Технолог'),
        Profession(name='Флорист'),
        Profession(name='Рыбак'),
        Profession(name='Испытатель водных горок'),
        Profession(name='Дрессировщик муравьёв'),
        Profession(name='Профессиональный обниматель панд'),
        Profession(name='Дегустатор мороженого'),
        Profession(name='Исследователь заброшенных мест'),
        Profession(name='Составитель кроссвордов'),
        Profession(name='Палеонтолог-любитель'),
        Profession(name='Специалист по выживанию в городе'),
        Profession(name='Модный критик уличного стиля'),
        Profession(name='Создатель механических кукол'),
        Profession(name='Куратор музея иллюзий'),
        Profession(name='Дегустатор чая'),
        Profession(name='Эксперт по инопланетным цивилизациям'),
        Profession(name='Астроном-любитель'),
        Profession(name='Организатор фестивалей света'),
        Profession(name='Скульптор'),
    ]
    session.add_all(professions)
    session.commit()
    session.close()
    print("Таблица профессий успешно заполнена.")

def populate_biology():
    session = Session()
    biology_entries = [
        Biology(gender='Мужчина', age=25, body_features='Высокий рост, спортивного телосложения'),
        Biology(gender='Женщина', age=30, body_features='Низкий рост, обычное телосложение'),
        Biology(gender='Женщина', age=69, body_features='Пожилая милфа среднего роста'),
        Biology(gender='Женщина', age=18, body_features='Средний рост, подросток'),
        Biology(gender='Мужчина', age=30, body_features='Низкий рост, среднего возраста'),
        Biology(gender='Женщина', age=69, body_features='Высокий рост, пожилая'),
        Biology(gender='Мужчина', age=99, body_features='Средний рост'),
        Biology(gender='Мужчина', age=40, body_features='Спортивное телосложение'),
        Biology(gender='Женщина', age=35, body_features='Хрупкое телосложение'),
        Biology(gender='Мужчина', age=28, body_features='Избыточный вес, средний рост'),
        Biology(gender='Женщина', age=22, body_features='Стройная фигура, низкий рост'),
        Biology(gender='Мужчина', age=34, body_features='Высокий рост, атлетическое телосложение'),
        Biology(gender='Женщина', age=28, body_features='Средний рост, стройная фигура'),
        Biology(gender='Мужчина', age=50, body_features='Низкий рост, крепкое телосложение, седые волосы'),
        Biology(gender='Женщина', age=45, body_features='Высокий рост, обычное телосложение, рыжие волосы'),
        Biology(gender='Мужчина', age=60, body_features='Средний рост, избыточный вес, носит очки'),
        Biology(gender='Женщина', age=33, body_features='Низкий рост, спортивное телосложение, темные волосы'),
        Biology(gender='Мужчина', age=25, body_features='Высокий рост, хрупкое телосложение, татуировки'),
        Biology(gender='Женщина', age=22, body_features='Средний рост, избыточный вес, зеленые глаза'),
        Biology(gender='Мужчина', age=40, body_features='Низкий рост, обычное телосложение, борода'),
        Biology(gender='Женщина', age=55, body_features='Высокий рост, стройная фигура, седые волосы'),
        Biology(gender='Мужчина', age=29, body_features='Средний рост, спортивное телосложение, светлые волосы'),
        Biology(gender='Женщина', age=37, body_features='Низкий рост, крепкое телосложение, носит очки'),
        Biology(gender='Мужчина', age=47, body_features='Высокий рост, избыточный вес, лысый'),
        Biology(gender='Женщина', age=19, body_features='Средний рост, хрупкое телосложение, длинные волосы'),
        Biology(gender='Мужчина', age=53, body_features='Низкий рост, обычное телосложение, темные волосы'),
        Biology(gender='Женщина', age=26, body_features='Высокий рост, спортивное телосложение, татуировки'),
        Biology(gender='Мужчина', age=31, body_features='Средний рост, стройное телосложение, карие глаза'),
        Biology(gender='Женщина', age=44, body_features='Низкий рост, избыточный вес, рыжие волосы'),
        Biology(gender='Мужчина', age=38, body_features='Высокий рост, крепкое телосложение, борода и усы'),
        Biology(gender='Женщина', age=60, body_features='Средний рост, обычное телосложение, седые волосы'),
    ]
    session.add_all(biology_entries)
    session.commit()
    session.close()
    print("Таблица биологических характеристик успешно заполнена.")

def populate_health():
    session = Session()
    health_entries = [
        Health(condition='Здоров'),
        Health(condition='Диабет'),
        Health(condition='Аллергия на пыльцу'),
        Health(condition='Проблемы со зрением'),
        Health(condition='Гипертония'),
        Health(condition='Астма'),
        Health(condition='Нимфоман(ка)'),
        Health(condition='Класустрофобия'),
        Health(condition='Гомосексуалист, но в остальном здоров'),
        Health(condition='Нету ручек'),
        Health(condition='Бесплодие'),
        Health(condition='Здоров'),
        Health(condition='Здоров'),
        Health(condition='Аллергия на орехи'),
        Health(condition='Астма'),
        Health(condition='Проблемы со слухом'),
        Health(condition='Гипертония'),
        Health(condition='Диабет II типа'),
        Health(condition='Здоров'),
        Health(condition='Депрессия'),
        Health(condition='Бессонница'),
        Health(condition='Ожирение'),
        Health(condition='Аритмия сердца'),
        Health(condition='Аллергия на пыльцу'),
        Health(condition='Здоров'),
        Health(condition='Травма колена'),
        Health(condition='Сколиоз'),
        Health(condition='Дальтонизм'),
        Health(condition='Анемия'),
        Health(condition='Здоров'),
        Health(condition='Хронический бронхит'),
        Health(condition='Панические атаки'),
        Health(condition='Клаустрофобия'),
        Health(condition='Потеря одного глаза'),
        Health(condition='Ампутация ноги'),
        Health(condition='Тревожное расстройство'),
        Health(condition='Агорафобия'),
        Health(condition='Дислексия'),
        Health(condition='Эпилепсия'),
        Health(condition='Синдром хронической усталости'),
        Health(condition='Остеохондроз'),
        Health(condition='Глаукома'),
        Health(condition='Гемофилия'),
        Health(condition='Проблемы с печенью'),
        Health(condition='Потеря обоняния'),
        Health(condition='Плоскостопие'),
        Health(condition='Хронический гастрит'),
        Health(condition='Плохое зрение'),
        Health(condition='Здоров'),
        Health(condition='Вегето-сосудистая дистония'),
        Health(condition='Посттравматическое стрессовое расстройство'),
        Health(condition='Гипотиреоз'),
        Health(condition='Бесплодие'),
        Health(condition='Импотенция'),
        Health(condition='Травма позвоночника'),
        Health(condition='Нарушение координации движений'),
        Health(condition='Проблемы с памятью'),
        Health(condition='Хроническая усталость'),
        Health(condition='Аллергия на животных'),
        Health(condition='Псориаз'),
        Health(condition='Нарушение речи'),
        Health(condition='Сниженный иммунитет'),
        Health(condition='Хроническая боль в спине'),
        Health(condition='Здоров'),
    ]
    session.add_all(health_entries)
    session.commit()
    session.close()
    print("Таблица состояний здоровья успешно заполнена.")

def populate_hobbies():
    session = Session()
    hobby_entries = [
        Hobby(hobby='Рыбалка'),
        Hobby(hobby='Чтение книг'),
        Hobby(hobby='Путешествия'),
        Hobby(hobby='Игра на гитаре'),
        Hobby(hobby='Рисование'),
        Hobby(hobby='Фотография'),
        Hobby(hobby='Спорт'),
        Hobby(hobby='Ботаника'),
        Hobby(hobby='Готовка'),
        Hobby(hobby='Коллекционирование марок'),
        Hobby(hobby='Скалолазание'),
        Hobby(hobby='Астрономия'),
        Hobby(hobby='Танцы'),
        Hobby(hobby='Медитация'),
        Hobby(hobby='Садоводство'),
        Hobby(hobby='Игры в шахматы'),
        Hobby(hobby='Косплей'),
        Hobby(hobby='Сочинение стихов'),
        Hobby(hobby='Гончарное дело'),
        Hobby(hobby='Виноделие'),
        Hobby(hobby='Ролевые настольные игры'),
        Hobby(hobby='Сёрфинг'),
        Hobby(hobby='Вышивание'),
        Hobby(hobby='Фехтование'),
        Hobby(hobby='Жонглирование'),
        Hobby(hobby='Пчеловодство'),
        Hobby(hobby='Фридайвинг'),
        Hobby(hobby='Генеалогия'),
        Hobby(hobby='Коллекционирование антиквариата'),
        Hobby(hobby='Моделирование'),
        Hobby(hobby='Кодирование'),
        Hobby(hobby='Кулинарные эксперименты'),
        Hobby(hobby='Изучение криптографии'),
        Hobby(hobby='Пение в хоре'),
        Hobby(hobby='Игра на редких музыкальных инструментах'),
        Hobby(hobby='Изучение мифологии'),
        Hobby(hobby='Фехтование на мечах'),
        Hobby(hobby='Походы в горы'),
        Hobby(hobby='Орнитология'),
        Hobby(hobby='Танец живота'),
        Hobby(hobby='Барабанный бой'),
        Hobby(hobby='Исторические реконструкции'),
        Hobby(hobby='Ледовая рыбалка'),
        Hobby(hobby='Сбор грибов'),
        Hobby(hobby='Гонки на дронах'),
        Hobby(hobby='Разведение экзотических растений'),
        Hobby(hobby='Посткроссинг'),
        Hobby(hobby='Создание настольных игр'),
        Hobby(hobby='Изучение иностранных языков'),
        Hobby(hobby='Кайтсерфинг'),
        Hobby(hobby='Садовая скульптура'),
        Hobby(hobby='Фрисби-гольф'),
        Hobby(hobby='Изготовление ювелирных изделий'),
        Hobby(hobby='Стрельба из лука'),
        Hobby(hobby='Караоке'),
        Hobby(hobby='Сольный поход'),
        Hobby(hobby='Аквариумистика'),
        Hobby(hobby='Авиамоделизм'),
        Hobby(hobby='Скалодром'),
        Hobby(hobby='Изготовление свечей'),
        Hobby(hobby='Татуировщик'),
        Hobby(hobby='Марафонский бег'),
        Hobby(hobby='Изучение философии'),
        Hobby(hobby='Экстремальный туризм'),
        Hobby(hobby='Плавание с аквалангом'),
        Hobby(hobby='Коллекционирование виниловых пластинок'),
        Hobby(hobby='Создание анимаций'),
        Hobby(hobby='Ведение блога'),
        Hobby(hobby='Пивоварение'),
        Hobby(hobby='Изучение истории моды'),
        Hobby(hobby='Флористика'),
        Hobby(hobby='Каллиграфия'),
        Hobby(hobby='Виртуальная реальность'),
        Hobby(hobby='Киберспорт'),
        Hobby(hobby='Генная инженерия (в теории)'),
        Hobby(hobby='Моделирование одежды'),
        Hobby(hobby='Изучение инопланетных теорий'),
        Hobby(hobby='Собирательство минералов'),
        Hobby(hobby='Археология (любительская)'),
        Hobby(hobby='Фотография дикой природы'),
        Hobby(hobby='Альпинизм'),
        Hobby(hobby='Квилтинг'),
        Hobby(hobby='Соление и маринование продуктов'),
        Hobby(hobby='Чайная церемония'),
        Hobby(hobby='Изучение картографии'),
        Hobby(hobby='Разведение бабочек'),
        Hobby(hobby='Аэрография'),
        Hobby(hobby='Психология личности'),
        Hobby(hobby='Тренировка собак'),
        Hobby(hobby='Изготовление мыла ручной работы'),
        Hobby(hobby='Эбру (рисование на воде)'),
        Hobby(hobby='Реставрация мебели'),
        Hobby(hobby='Участие в квизах и викторинах'),
        Hobby(hobby='Изучение иностранных культур'),
        Hobby(hobby='Паркур'),
        Hobby(hobby='Бонсай'),
        Hobby(hobby='Съемка короткометражных фильмов'),
        Hobby(hobby='Фехтование на шпагах'),
        Hobby(hobby='Песочная анимация'),
        Hobby(hobby='Изготовление бумажных фигурок (оригами)'),
        Hobby(hobby='Кулинарные путешествия'),
        Hobby(hobby='Участие в флешмобах'),
        Hobby(hobby='Изучение астрологии'),
        Hobby(hobby='Занятия йогой'),
        Hobby(hobby='Бег с препятствиями'),
        Hobby(hobby='Рыбалка'),
        Hobby(hobby='Чтение книг'),
        Hobby(hobby='Путешествия'),
        Hobby(hobby='Игра на гитаре'),
        Hobby(hobby='Рисование'),
        Hobby(hobby='Фотография'),
        Hobby(hobby='Коллекционирование пыли'),
        Hobby(hobby='Смотрение в потолок'),
        Hobby(hobby='Перекладывание бумаг на столе'),
        Hobby(hobby='Спорт'),
        Hobby(hobby='Ботаника'),
        Hobby(hobby='Готовка'),
        Hobby(hobby='Прокрастинация'),
        Hobby(hobby='Собирание пустых бутылок'),
        Hobby(hobby='Чтение сплетен в журналах'),
        Hobby(hobby='Саркастические комментарии в интернете'),
        Hobby(hobby='Избегание ответственности'),
        Hobby(hobby='Коллекционирование бесполезных гаджетов'),
        Hobby(hobby='Бесцельное блуждание по городу'),
        Hobby(hobby='Составление списков, которые никогда не используются'),
        Hobby(hobby='Перебивание собеседника'),
        Hobby(hobby='Постоянные жалобы на погоду'),
        Hobby(hobby='Излишняя критичность ко всему'),
        Hobby(hobby='Откладывание важных дел на потом'),
        Hobby(hobby='Пассивное наблюдение за жизнью других'),
        Hobby(hobby='Изучение языков, которые не планируешь использовать'),
        Hobby(hobby='Сидение в социальных сетях часами'),
        Hobby(hobby='Сарказм в общении'),
        Hobby(hobby='Избегание социальных контактов'),
        Hobby(hobby='Просмотр сериалов без остановки'),
        Hobby(hobby='Пустая трата времени в мобильных играх'),
        Hobby(hobby='Коллекционирование ненужных вещей'),
        Hobby(hobby='Чрезмерный шопинг'),
        Hobby(hobby='Перекладывание вины на других'),
        Hobby(hobby='Сон в неудобное время'),
        Hobby(hobby='Чтение спойлеров к фильмам и рассказ другим'),
        Hobby(hobby='Троллинг в интернете'),
        Hobby(hobby='Бездумное переключение телевизионных каналов'),
        Hobby(hobby='Поедание фастфуда'),
        Hobby(hobby='Нарушение режима сна'),
        Hobby(hobby='Чрезмерный пессимизм'),
        Hobby(hobby='Безделье'),
        Hobby(hobby='Отрицание собственных ошибок'),
        Hobby(hobby='Неумеренное потребление сладкого'),
        Hobby(hobby='Излишняя самокритика'),
        Hobby(hobby='Игнорирование советов других'),
        Hobby(hobby='Склонность к драматизации событий'),
        Hobby(hobby='Постоянное сравнение себя с другими'),
        Hobby(hobby='Собирание пыли на полках'),
        Hobby(hobby='Бесцельное прослушивание музыки без наслаждения'),
        Hobby(hobby='Изучение ненужных фактов'),
    ]
    session.add_all(hobby_entries)
    session.commit()
    session.close()
    print("Таблица хобби успешно заполнена.")

def populate_luggage():
    session = Session()
    luggage_entries = [
        Luggage(item='Аптечка'),
        Luggage(item='Набор инструментов'),
        Luggage(item='Спальный мешок'),
        Luggage(item='Запас еды'),
        Luggage(item='Карта местности'),
        Luggage(item='Нож'),
        Luggage(item='Пистлет с одним патроном'),
        Luggage(item='Пачка патронов'),
        Luggage(item='Презервативы'),
        Luggage(item='Карта бункеров города'),
        Luggage(item='Резиновый член'),
        Luggage(item='Набор провизии на неделю'),
        Luggage(item='Бинокль'),
        Luggage(item='Костюм хим защиты (хз откудо)'),
        Luggage(item='Инвалидная коляска'),
        Luggage(item='Фонарик'),
        Luggage(item='Сломанный компас, который всегда указывает на юг'),
        Luggage(item='Пустая бутылка, фольга и спички'),
        Luggage(item='Набор ложек без вилок'),
        Luggage(item='Книга "1000 способов приготовить картофель", 999 страниц отсутствуют'),
        Luggage(item='Ключ для любой двери'),
        Luggage(item='Футбольный мяч с автографом известного спортсмена'),
        Luggage(item='Коллекция марок из вымышленных стран'),
        Luggage(item='Зонт без ткани, только спицы'),
        Luggage(item='Карта метро города, в котором вы никогда не были'),
        Luggage(item='Пачка игральных карт без тузов'),
        Luggage(item='Набор пустых бутылок из-под дорогого вина'),
        Luggage(item='Ключи от автомобиля без автомобиля'),
        Luggage(item='Запасная шнуровка для ботинок'),
        Luggage(item='Ручной вентилятор без батареек'),
        Luggage(item='Банка консервов без открывалки'),
        Luggage(item='Радио, которое ловит только одну станцию на китайском языке'),
        Luggage(item='Солнечные очки с одной линзой'),
        Luggage(item='Лампочка'),
        Luggage(item='Сломанный будильник, который звонит в случайное время'),
        Luggage(item='Перо страуса, украшенное золотом'),
    ]
    session.add_all(luggage_entries)
    session.commit()
    session.close()
    print("Таблица багажа успешно заполнена.")

def populate_facts():
    session = Session()
    fact_entries =  [
        Fact(fact='Был спасателем'),
        Fact(fact='Знает 3 иностранных языка'),
        Fact(fact='Имеет черный пояс по карате'),
        Fact(fact='Был в Антарктиде и дрался с белым медведем'),
        Fact(fact='Может выживать в дикой природе'),
        Fact(fact='Имеет опыт работы в лаборатории. Ученик самого Хайзенберга'),
        Fact(fact='Занимается сексом как бог'),
        Fact(fact='Студент КазНПУ(Выжил в общежитии)'),
        Fact(fact='Картограф'),
        Fact(fact='Топографический кретинизм'),
        Fact(fact='Вампир'),
        Fact(fact='Был охотником'),
        Fact(fact='Был капитаном дальнего плавания'),
        Fact(fact='Знает 5 иностранных языков и язык фактов'),
        Fact(fact='Имеет опыт выживания в джунглях Амазонки'),
        Fact(fact='Участвовал в международных шахматных турнирах'),
        Fact(fact='Был профессиональным альпинистом'),
        Fact(fact='Изобрел новый вид топлива из слез'),
        Fact(fact='Обладатель черного пояса по джиу-джитсу'),
        Fact(fact='Был участником олимпийской сборной по плаванию'),
        Fact(fact='Имеет степень доктора наук в области порнографии '),
        Fact(fact='Может приготовить еду из любых доступных ингредиентов'),
        Fact(fact='Опытный механик и автомастер'),
        Fact(fact='Работал в службе спасения МЧС'),
        Fact(fact='Имеет навыки первой медицинской помощи'),
        Fact(fact='Был в космосе как астронавт'),
        Fact(fact='Может ориентироваться по звездам'),
        Fact(fact='Вышел за хлебом и не вернулся'),
        Fact(fact='Занимается паркуром'),
        Fact(fact='Бывший сотрудник спецназа'),
        Fact(fact='Имеет опыт работы с взрывчатыми веществами'),
        Fact(fact='Разработчик программного обеспечения с опытом в кибербезопасности'),
        Fact(fact='Был инструктором по йоге и медитации'),
        Fact(fact='Профессиональный садовник и ботаник'),
        Fact(fact='Имеет опыт работы ветеринаром'),
        Fact(fact='Специалист по радиосвязи и телекоммуникациям'),
        Fact(fact='Был пожарным спасателем'),
        Fact(fact='Умеет управлять различными видами транспорта'),
        Fact(fact='Имеет опыт работы пчеловодом'),
        Fact(fact='Бывший шеф-повар известного ресторана Ланджоу'),
        Fact(fact='Знает секреты традиционной медицины'),
        Fact(fact='Обладатель феноменальной памяти'),
        Fact(fact='Имеет опыт строительства и ремонта зданий'),
        Fact(fact='Был профессиональным маскировщиком'),
        Fact(fact='Может создавать оружие из другого оружия'),
        Fact(fact='Имеет опыт в гидропонике и выращивании растений'),
        Fact(fact='Бывший дипломат со связями по всему миру'),
        Fact(fact='Опытный следопыт и знаток дикой природы'),
        Fact(fact='Имеет навыки гипноза и психологии'),
        Fact(fact='Был участником кругосветного путешествия на яхте'),
        Fact(fact='Специалист по альтернативным источникам энергии'),
        Fact(fact='Может собрать компьютер из деталей лего'),
        Fact(fact='Бывший чемпион по стрельбе из лука'),
        Fact(fact='Имеет опыт работы археологом'),
        Fact(fact='Знает основы токсикологии и ядовитых растений'),
        Fact(fact='Мастер по изготовлению одежды и обуви'),
        Fact(fact='Имеет навыки художественного искусства и дизайна'),
        Fact(fact='Может общаться с животными, но нужна травка (обоим)'),
        Fact(fact='Обладатель феноменального слуха'),
        Fact(fact='Был профессиональным барменом и знает множество рецептов напитков'),
        Fact(fact='Имеет опыт работы в подводных исследованиях'),
        Fact(fact='Может читать карты, но не умеет пользоваться компасом'),
        Fact(fact='Знает основы электротехники'),

    ]
    session.add_all(fact_entries)
    session.commit()
    session.close()
    print("Таблица фактов успешно заполнена.")

def populate_locations():
    session = Session()
    location_entries = [
        Location( 
            description='Глобальная засуха, город Астана в 2065 году.', 
            survival_conditions='Из-за изменения климата водные ресурсы иссякли. Город окружен пустыней, и выжившие борются за оставшиеся запасы воды и пищи. Необходимо организовать добычу воды из подземных источников и защищаться от бандитов, охотящихся за ресурсами.' 
        ),
Location(
    description='Извержение супервулкана, город Неаполь, Италия в 2040 году.', 
    survival_conditions='После катастрофического извержения вулкана Везувий город покрыт слоем пепла. Солнце скрыто за облаками вулканической пыли, температуры резко упали — началась "вулканическая зима". Выжившие должны найти способы согреться, добывать пищу в условиях отсутствия солнечного света и избежать токсичных газов.'
),

Location(
    description='Глобальная пандемия, Токио, Япония в 2025 году.', 
    survival_conditions='Неизвестный вирус распространился по всему миру, заражая миллионы. Город на строгом карантине, ресурсы ограничены, инфраструктура рушится. Выжившие должны избегать зараженных, искать лекарства и поддерживать связь с внешним миром для возможной эвакуации.'
),

Location(
    description='Мегаземлетрясение, Сан-Франциско, США в 2032 году.', 
    survival_conditions='Сильное землетрясение разрушило город, коммуникации нарушены, повсюду пожары и обрушения. Выжившие должны искать безопасные места, добывать воду и пищу среди руин и избегать мародеров, пользующихся хаосом.'
),

Location(
    description='Инопланетное вторжение, Каир, Египет в 2077 году.', 
    survival_conditions='Земля подверглась нападению внеземной расы, и Каир стал эпицентром боевых действий. Выжившие прячутся в древних пирамидах и подземных катакомбах, пытаясь найти способ противостоять технологиям захватчиков и защитить свою планету.'
),

Location(
    description='Полярный сдвиг, Москва, Россия в 2100 году.', 
    survival_conditions='Магнитные полюса Земли сместились, что привело к климатическим аномалиям. Москва оказалась во власти вечной зимы. Выжившие должны бороться с экстремальным холодом, искать топливо и пищу, а также избегать новых опасных хищников, мигрировавших из арктических регионов.'
),

Location(
    description='Кибернетический коллапс, Сеул, Южная Корея в 2050 году.', 
    survival_conditions='Глобальная сеть искусственного интеллекта вышла из-под контроля, захватив управление инфраструктурой города. Электронные системы стали враждебными к человеку. Выжившие должны обходиться без технологий, использовать механические устройства и укрываться от дронов-охотников.'
),

Location(
    description='Гигантское цунами, Сидней, Австралия в 2085 году.', 
    survival_conditions='После падения метеорита в Тихий океан огромная волна затопила прибрежные города. Сидней под водой, лишь верхушки небоскребов выступают над поверхностью. Выжившие ищут спасение на высотных зданиях, борются за запасы пресной воды и пищи, а также сталкиваются с морскими хищниками, обитающими теперь в городе.'
),

Location(
    description='Солнечная вспышка, Нью-Йорк, США в 2060 году.', 
    survival_conditions='Мощная солнечная вспышка уничтожила все электронные устройства. Город погрузился в хаос без связи, транспорта и электричества. Выжившие должны вернуться к примитивным методам выживания, добывать пищу и воду вручную, а также защищаться от группировок, стремящихся установить контроль над ресурсами.'
),

Location(
    description='Эпидемия зомби, Рио-де-Жанейро, Бразилия в 2035 году.', 
    survival_conditions='Неизвестный вирус превратил большую часть населения в агрессивных зомби. Выжившие должны скрываться в джунглях и горах, искать безопасные убежища, добывать пищу и оружие и, возможно, найти способ остановить распространение вируса.'
),

Location(
    description='Биологический катаклизм, Шанхай, Китай в 2090 году.', 
    survival_conditions='Из-за генетического эксперимента растения стали быстро расти и захватывать города. Шанхай превратился в зеленые джунгли с гигантскими растениями, некоторые из которых опасны для человека. Выжившие должны пробираться через густые заросли, искать пищу и воду, избегать опасных растений и найти способ остановить биологическую экспансию.'
),
    ]
    session.add_all(location_entries)
    session.commit()
    session.close()
    print("Таблица локаций успешно заполнена.")

def populate_phobias():
    session = Session()
    phobia_entries = [
    Phobia(phobia='Боязнь высоты'),
    Phobia(phobia='Клаустрофобия'),            # Боязнь замкнутых пространств
    Phobia(phobia='Боязнь темноты'),
    Phobia(phobia='Боязнь воды'),
    Phobia(phobia='Арахнофобия'),              # Боязнь пауков
    Phobia(phobia='Боязнь змей'),
    Phobia(phobia='Боязнь крови'),
    Phobia(phobia='Боязнь собак'),
    Phobia(phobia='Боязнь насекомых'),
    Phobia(phobia='Боязнь громких звуков'),
    Phobia(phobia='Социофобия'),               # Боязнь социальных ситуаций
    Phobia(phobia='Боязнь полетов'),
    Phobia(phobia='Боязнь микробов'),
    Phobia(phobia='Боязнь публичных выступлений'),
    Phobia(phobia='Боязнь смерти'),
]

    session.add_all(phobia_entries)
    session.commit()
    session.close()
    print("Таблица фобий успешно заполнена.")

def populate_talents():
    session = Session()
    talent_entries = [
        Talent(talent='Игра на фортепиано'),
        Talent(talent='Пение'),
        Talent(talent='Быстрое обучение'),
        Talent(talent='Математический гений'),
        Talent(talent='Художественный талант')
    ]
    session.add_all(talent_entries)
    session.commit()
    session.close()
    print("Таблица талантов успешно заполнена.")

def populate_social_statuses():
    session = Session()
    status_entries = [
    SocialStatus(status='Богач'),
    SocialStatus(status='Средний класс'),
    SocialStatus(status='Бедняк'),
    SocialStatus(status='Аристократ'),
    SocialStatus(status='Безработный'),
    SocialStatus(status='Студент'),
    SocialStatus(status='Предприниматель'),
    SocialStatus(status='Фрилансер'),
    SocialStatus(status='Самозанятый'),
    SocialStatus(status='Владелец бизнеса'),
    SocialStatus(status='Религиозный деятель'),
    SocialStatus(status='Активист'),
    SocialStatus(status='Геймер'),
    SocialStatus(status='Коллекционер'),
    SocialStatus(status='Волонтер'),
    SocialStatus(status='Старший менеджер'),
    SocialStatus(status='Младший специалист'),
]

    session.add_all(status_entries)
    session.commit()
    session.close()
    print("Таблица социального статуса успешно заполнена.")

def populate_achievements():
    session = Session()
    achievement_entries = [
        Achievement(name='Первая победа', description='Победите в игре впервые.'),
        Achievement(name='Участник', description='Примите участие в 5 играх.'),
        Achievement(name='Победитель', description='Победите в 10 играх.')
    ]
    session.add_all(achievement_entries)
    session.commit()
    session.close()
    print("Таблица достижений успешно заполнена.")

if __name__ == '__main__':
    create_tables()
    populate_professions()
    populate_biology()
    populate_health()
    populate_hobbies()
    populate_luggage()
    populate_facts()
    populate_locations()
    populate_phobias()
    populate_talents()
    populate_social_statuses()
    populate_achievements()
    print("База данных успешно заполнена.")
