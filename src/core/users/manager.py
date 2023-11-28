from __future__ import annotations
from typing import TYPE_CHECKING
from datetime import datetime

from fastapi_users import BaseUserManager, IntegerIDMixin
from src.core.users.models import User
from src.core.config import get_settings
from src.core.users.schemas import UserUpdate


if TYPE_CHECKING:
    from fastapi import Request
    from starlette.responses import Response
    from fastapi_users.models import UP


settings = get_settings()


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = settings.SECRET_KEY
    verification_token_secret = settings.SECRET_KEY

    async def on_after_login(
        self,
        user: UP,
        request: Request | None = None,
        response: Response | None = None,
    ) -> None:
        update_json = user.to_json()
        update_json["last_login"] = datetime.now()

        await self.update(UserUpdate(**update_json), user, safe=True, request=request)
