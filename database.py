# database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///bunker_game.db', echo=False)
Session = sessionmaker(bind=engine)

def init_db():
    from models import Base
    Base.metadata.create_all(engine)
