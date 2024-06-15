# database.py

from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_FILENAME = 'game_state.db'
Base = declarative_base()

class GameState(Base):
    __tablename__ = 'game_state'
    id = Column(Integer, primary_key=True)
    slot = Column(Integer, unique=True)
    day = Column(Integer)
    money = Column(Integer)
    left_maneuvering_engine = Column(Boolean)
    right_maneuvering_engine = Column(Boolean)
    engine_efficiency = Column(Boolean)
    engine_power = Column(Boolean)

def initialize_database():
    if not os.path.exists(DATABASE_FILENAME):
        engine = create_engine(f'sqlite:///{DATABASE_FILENAME}')
        Base.metadata.create_all(engine)

def get_session():
    engine = create_engine(f'sqlite:///{DATABASE_FILENAME}')
    Session = sessionmaker(bind=engine)
    return Session()

def save_game_state(slot, day, player):
    session = get_session()
    game_state = session.query(GameState).filter_by(slot=slot).first()
    if not game_state:
        game_state = GameState(slot=slot)

    game_state.day = day
    game_state.money = player.money
    game_state.left_maneuvering_engine = player.player_upgrades["Left_maneuvering_engine"]
    game_state.right_maneuvering_engine = player.player_upgrades["Right_maneuvering_engine"]
    game_state.engine_efficiency = player.player_upgrades["Engine_efficiency"]
    game_state.engine_power = player.player_upgrades["Engine_power"]

    session.add(game_state)
    session.commit()

def load_game_state(slot):
    session = get_session()
    game_state = session.query(GameState).filter_by(slot=slot).first()
    if game_state:
        return {
            'day': game_state.day,
            'money': game_state.money,
            'upgrades': {
                "Left_maneuvering_engine": game_state.left_maneuvering_engine,
                "Right_maneuvering_engine": game_state.right_maneuvering_engine,
                "Engine_efficiency": game_state.engine_efficiency,
                "Engine_power": game_state.engine_power
            }
        }
    return None

def get_save_slots():
    session = get_session()
    slots = session.query(GameState.slot, GameState.day).all()
    return {slot: day for slot, day in slots}


def delete_all_saves():
    session = get_session()
    try:
        session.query(GameState).delete()
        session.commit()
        print("All saves deleted.")
    except Exception as e:
        session.rollback()
        print(f"Error deleting saves: {e}")
    finally:
        session.close()