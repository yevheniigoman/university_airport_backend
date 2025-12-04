from config import get_settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(get_settings().DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)