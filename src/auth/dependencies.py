from dependencies import get_async_session
from models import User
from .manager import UserManager
from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.orm import Session
from typing import Generator


def get_user_db(
    session: Session = Depends(get_async_session)
) -> Generator[SQLAlchemyUserDatabase]:
    yield SQLAlchemyUserDatabase(session, User)

def get_user_manager(user_db = Depends(get_user_db)) -> UserManager:
    return UserManager(user_db)
