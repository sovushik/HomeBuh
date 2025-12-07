from sqlmodel import SQLModel, create_engine, Session
from pathlib import Path

DB_FILE = Path(__file__).resolve().parent / "data.db"
engine = create_engine(f"sqlite:///{DB_FILE}", echo=False, connect_args={"check_same_thread": False})

def init_db():
    from .models import *  # noqa: F401
    SQLModel.metadata.create_all(engine)

def get_session():
    return Session(engine)
