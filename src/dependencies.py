from db import SessionLocal
from sqlalchemy.orm import Session
from typing import Generator

def get_session():
    with SessionLocal() as session:
        yield session