from dependencies import get_session
from models import User
from .manager import UserManager
from fastapi import Depends
from fastapi_users_db_sync_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.orm import Session
from typing import Generator


def get_user_db(
    session: Session = Depends(get_session)
):
    yield SQLAlchemyUserDatabase(session, User)

def get_user_manager(user_db = Depends(get_user_db)) -> UserManager:
    return UserManager(user_db)
