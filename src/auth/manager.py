from config import get_settings
from models import User
from fastapi_users import BaseUserManager, IntegerIDMixin


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = get_settings().SECRET
    verification_token_secret = get_settings().SECRET
