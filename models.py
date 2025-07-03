# models.py

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column, Integer, String, ForeignKey, Boolean,
    Text, DateTime, func
)
from sqlalchemy.orm import relationship

# Базовый класс для всех моделей SQLAlchemy
Base = declarative_base()

class Player(Base):
    """
    Модель, представляющая игрока.
    Хранит информацию о пользователе Telegram, его статистику и текущее состояние в игре.
    """
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, index=True, nullable=False, doc="Уникальный идентификатор пользователя в Telegram")
    username = Column(String, nullable=False, doc="Имя пользователя в Telegram")
    wins = Column(Integer, default=0, doc="Количество побед")
    losses = Column(Integer, default=0, doc="Количество поражений")
    
    # Связь с текущей комнатой игрока
    current_room_id = Column(Integer, ForeignKey('rooms.id'), index=True, doc="ID комнаты, в которой находится игрок")
    room = relationship("Room", back_populates="players", foreign_keys=[current_room_id])

    # Отношение "один-к-одному" с характеристиками
    characteristics = relationship("Characteristic", uselist=False, back_populates="player", cascade="all, delete-orphan")
    
    # Отношение "один-ко-многим" с достижениями
    achievements = relationship("PlayerAchievement", back_populates="player", cascade="all, delete-orphan")
    
    # Связи для отправленных и полученных сообщений
    sent_messages = relationship("Message", foreign_keys='Message.sender_id', back_populates="sender")
    received_messages = relationship("Message", foreign_keys='Message.recipient_id', back_populates="recipient")

class Room(Base):
    """
    Модель, представляющая игровую комнату.
    Содержит информацию о комнате, ее участниках и состоянии игры.
    """
    __tablename__ = 'rooms'

    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True, index=True, nullable=False, doc="Уникальный код для присоединения к комнате")
    host_id = Column(Integer, ForeignKey('players.id'), nullable=False, doc="ID игрока, который является хостом комнаты")
    is_active = Column(Boolean, default=True, doc="Активна ли комната в данный момент")
    is_voting = Column(Boolean, default=False, doc="Идет ли в комнате голосование")
    max_players = Column(Integer, default=15, doc="Максимальное количество игроков")
    survivors = Column(Integer, default=2, doc="Количество выживших для завершения игры")
    
    # Связь с локацией (катастрофой)
    location_id = Column(Integer, ForeignKey('locations.id'), doc="ID текущей локации/катастрофы")
    location = relationship("Location", back_populates="rooms")
    
    # Связь с хостом комнаты
    host = relationship("Player", foreign_keys=[host_id], backref="hosted_rooms")
    
    # Игроки в комнате
    players = relationship("Player", back_populates="room", foreign_keys=[Player.current_room_id])
    
    # Связанные сообщения и голоса (удаляются вместе с комнатой)
    messages = relationship("Message", back_populates="room", cascade="all, delete-orphan")
    votes = relationship("Vote", back_populates="room", cascade="all, delete-orphan")

class Characteristic(Base):
    """
    Модель для хранения сгенерированных характеристик персонажа для одного игрока.
    """
    __tablename__ = 'characteristics'

    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('players.id'), unique=True, nullable=False)
    profession = Column(String)
    biology = Column(String)
    health = Column(String)
    hobby = Column(String)
    luggage = Column(String)
    facts = Column(String)
    phobia = Column(String)
    talent = Column(String)
    social_status = Column(String)
    
    player = relationship("Player", back_populates="characteristics")

class Vote(Base):
    """
    Модель для учета голоса одного игрока в раунде голосования.
    """
    __tablename__ = 'votes'

    id = Column(Integer, primary_key=True)
    room_id = Column(Integer, ForeignKey('rooms.id'), nullable=False, index=True)
    voter_id = Column(Integer, ForeignKey('players.id'), nullable=False, doc="ID голосующего игрока")
    voted_player_id = Column(Integer, ForeignKey('players.id'), nullable=False, doc="ID игрока, против которого проголосовали")
    
    room = relationship("Room", back_populates="votes")
    voter = relationship("Player", foreign_keys=[voter_id])
    voted_player = relationship("Player", foreign_keys=[voted_player_id])

class Message(Base):
    """
    Модель для хранения одного сообщения в чате (общем или приватном).
    """
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    room_id = Column(Integer, ForeignKey('rooms.id'), nullable=False, index=True)
    sender_id = Column(Integer, ForeignKey('players.id'), nullable=False)
    recipient_id = Column(Integer, ForeignKey('players.id'), nullable=True, doc="Если NULL, сообщение для всех в комнате")
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), doc="Время отправки сообщения")
    
    room = relationship("Room", back_populates="messages")
    sender = relationship("Player", foreign_keys=[sender_id], back_populates="sent_messages")
    recipient = relationship("Player", foreign_keys=[recipient_id], back_populates="received_messages")

# --- Таблицы-справочники для генерации характеристик ---

class Location(Base):
    """Справочник катастроф и условий выживания."""
    __tablename__ = 'locations'
    id = Column(Integer, primary_key=True)
    description = Column(Text, nullable=False)
    survival_conditions = Column(Text, nullable=False)
    rooms = relationship("Room", back_populates="location")

class Profession(Base):
    """Справочник профессий."""
    __tablename__ = 'professions'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

class Biology(Base):
    """Справочник биологических данных."""
    __tablename__ = 'biology'
    id = Column(Integer, primary_key=True)
    gender = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    body_features = Column(String, nullable=False)

class Health(Base):
    """Справочник состояний здоровья."""
    __tablename__ = 'health'
    id = Column(Integer, primary_key=True)
    condition = Column(String, nullable=False)

class Hobby(Base):
    """Справочник хобби."""
    __tablename__ = 'hobbies'
    id = Column(Integer, primary_key=True)
    hobby = Column(String, nullable=False)

class Luggage(Base):
    """Справочник предметов в багаже."""
    __tablename__ = 'luggage'
    id = Column(Integer, primary_key=True)
    item = Column(String, nullable=False)

class Fact(Base):
    """Справочник интересных фактов о персонаже."""
    __tablename__ = 'facts'
    id = Column(Integer, primary_key=True)
    fact = Column(String, nullable=False)

class Phobia(Base):
    """Справочник фобий."""
    __tablename__ = 'phobias'
    id = Column(Integer, primary_key=True)
    phobia = Column(String, nullable=False)

class Talent(Base):
    """Справочник талантов."""
    __tablename__ = 'talents'
    id = Column(Integer, primary_key=True)
    talent = Column(String, nullable=False)

class SocialStatus(Base):
    """Справочник социальных статусов."""
    __tablename__ = 'social_statuses'
    id = Column(Integer, primary_key=True)
    status = Column(String, nullable=False)

# --- Система достижений ---

class Achievement(Base):
    """
    Модель, описывающая возможное достижение в игре.
    """
    __tablename__ = 'achievements'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(Text, nullable=False)
    
    players = relationship("PlayerAchievement", back_populates="achievement")

class PlayerAchievement(Base):
    """
    Ассоциативная таблица, связывающая игрока и полученное им достижение.
    """
    __tablename__ = 'player_achievements'

    player_id = Column(Integer, ForeignKey('players.id'), primary_key=True)
    achievement_id = Column(Integer, ForeignKey('achievements.id'), primary_key=True)
    date_achieved = Column(DateTime(timezone=True), server_default=func.now())
    
    player = relationship("Player", back_populates="achievements")
    achievement = relationship("Achievement", back_populates="players")