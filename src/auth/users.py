from models import User
from .dependencies import get_user_manager
from .backend import auth_backend
from fastapi_users import FastAPIUsers


fastapi_auth = FastAPIUsers[User, int](get_user_manager, [auth_backend])

get_current_active_user = fastapi_auth.current_user(active=True)
