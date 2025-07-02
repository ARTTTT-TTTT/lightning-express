from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from app.configs.app_config import app_config

DATABASE_URL = str(app_config.SQLALCHEMY_DATABASE_URI)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

try:
    with engine.connect() as connection:
        print("🚀 Connected to postgreSQL")
except Exception as e:
    print("Failed to connect to database:", e)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
