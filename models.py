# models.py

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Player(Base):
    __tablename__ = 'players'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True)
    username = Column(String)
    wins = Column(Integer, default=0)
    losses = Column(Integer, default=0)
    current_room_id = Column(Integer, ForeignKey('rooms.id'))
    
    characteristics = relationship("Characteristic", uselist=False, back_populates="player")
    achievements = relationship("PlayerAchievement", back_populates="player")
    
    sent_messages = relationship("Message", foreign_keys='Message.sender_id', back_populates="sender")
    received_messages = relationship("Message", foreign_keys='Message.recipient_id', back_populates="recipient")
    
    room = relationship("Room", back_populates="players", foreign_keys='Player.current_room_id')

class Room(Base):
    __tablename__ = 'rooms'
    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True)
    host_id = Column(Integer, ForeignKey('players.id'))
    is_active = Column(Boolean, default=True)
    max_players = Column(Integer)
    survivors = Column(Integer)
    location_id = Column(Integer, ForeignKey('locations.id'))
    is_voting = Column(Boolean, default=False)
    
    # Явно указываем внешний ключ для хоста
    host = relationship("Player", foreign_keys=[host_id], backref="hosted_rooms")
    
    # Явно указываем внешний ключ для игроков в комнате
    players = relationship("Player", back_populates="room", foreign_keys='Player.current_room_id')
    
    messages = relationship("Message", back_populates="room")
    votes = relationship("Vote", back_populates="room")
    location = relationship("Location", back_populates="room")

class Characteristic(Base):
    __tablename__ = 'characteristics'
    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('players.id'))
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

class Location(Base):
    __tablename__ = 'locations'
    id = Column(Integer, primary_key=True)
    description = Column(Text)
    survival_conditions = Column(Text)
    
    room = relationship("Room", back_populates="location")

class Vote(Base):
    __tablename__ = 'votes'
    id = Column(Integer, primary_key=True)
    room_id = Column(Integer, ForeignKey('rooms.id'))
    voter_id = Column(Integer, ForeignKey('players.id'))
    voted_player_id = Column(Integer, ForeignKey('players.id'))
    
    room = relationship("Room", back_populates="votes")
    voter = relationship("Player", foreign_keys=[voter_id])
    voted_player = relationship("Player", foreign_keys=[voted_player_id])

class Profession(Base):
    __tablename__ = 'professions'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

class Biology(Base):
    __tablename__ = 'biology'
    id = Column(Integer, primary_key=True)
    gender = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    body_features = Column(String, nullable=False)

class Health(Base):
    __tablename__ = 'health'
    id = Column(Integer, primary_key=True)
    condition = Column(String, nullable=False)

class Hobby(Base):
    __tablename__ = 'hobbies'
    id = Column(Integer, primary_key=True)
    hobby = Column(String, nullable=False)

class Luggage(Base):
    __tablename__ = 'luggage'
    id = Column(Integer, primary_key=True)
    item = Column(String, nullable=False)

class Fact(Base):
    __tablename__ = 'facts'
    id = Column(Integer, primary_key=True)
    fact = Column(String, nullable=False)

class Phobia(Base):
    __tablename__ = 'phobias'
    id = Column(Integer, primary_key=True)
    phobia = Column(String, nullable=False)

class Talent(Base):
    __tablename__ = 'talents'
    id = Column(Integer, primary_key=True)
    talent = Column(String, nullable=False)

class SocialStatus(Base):
    __tablename__ = 'social_statuses'
    id = Column(Integer, primary_key=True)
    status = Column(String, nullable=False)

class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    room_id = Column(Integer, ForeignKey('rooms.id'))
    sender_id = Column(Integer, ForeignKey('players.id'))
    recipient_id = Column(Integer, ForeignKey('players.id'), nullable=True)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    room = relationship("Room", back_populates="messages")
    sender = relationship("Player", foreign_keys=[sender_id], back_populates="sent_messages")
    recipient = relationship("Player", foreign_keys=[recipient_id], back_populates="received_messages")

class Achievement(Base):
    __tablename__ = 'achievements'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    
    players = relationship("PlayerAchievement", back_populates="achievement")

class PlayerAchievement(Base):
    __tablename__ = 'player_achievements'
    player_id = Column(Integer, ForeignKey('players.id'), primary_key=True)
    achievement_id = Column(Integer, ForeignKey('achievements.id'), primary_key=True)
    date_achieved = Column(DateTime, default=datetime.utcnow)
    
    player = relationship("Player", back_populates="achievements")
    achievement = relationship("Achievement", back_populates="players")
