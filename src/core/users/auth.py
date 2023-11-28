from fastapi_users.authentication import (
    BearerTransport,
    JWTStrategy,
    AuthenticationBackend,
)
from src.core.users.utils import get_user_manager
from src.core.users.models import User
from fastapi_users import FastAPIUsers
from src.core.users.schemas import UserRead, UserCreate, UserUpdate
from src.core.config import get_settings

settings = get_settings()


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=settings.SECRET_KEY,
        lifetime_seconds=settings.ACCESS_TOKEN_EXPIRE_SECONDS,
    )


bearer_transport = BearerTransport(
    tokenUrl=settings.BASE_API_PREFIX + "/auth/jwt/login",
)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

auth_router = fastapi_users.get_auth_router(backend=auth_backend)
register_router = fastapi_users.get_register_router(UserRead, UserCreate)
users_router = fastapi_users.get_users_router(UserRead, UserUpdate)
