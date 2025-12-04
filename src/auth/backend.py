from config import get_settings
from fastapi_users.authentication import (
    CookieTransport, JWTStrategy, AuthenticationBackend
)


cookie_transport = CookieTransport()

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=get_settings().SECRET, lifetime_seconds=3600)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy
)
