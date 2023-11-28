from fastapi import FastAPI, Depends
from src.core.users.auth import (
    auth_router,
    register_router,
    users_router,
    fastapi_users,
)
from src.core.users.models import User
from src.core.config import get_settings

description = """
# Статус - в разработке ⚙️

## Краткое описание 📃

* ### Данное API предназначено для реализации функционала онлайн-платформы, где будет происходить **купля-продажа товаров** ✅
* ### Функционал предусматривает **оформление заказа** и безопасное, точное доведение его до покупателя ✅
* ### Сервис подходит для **высоких нагрузок** и может работать с большим кол-вом пользователей одновременно ✅
"""


settings = get_settings()


class YshopAPI(FastAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.router.prefix = settings.BASE_API_PREFIX


app = YshopAPI(
    debug=settings.DEBUG,
    description=description,
    title=settings.PROJECT_NAME,
    docs_url=settings.BASE_API_PREFIX + "/docs",
    version=str(settings.API_VERSION_INT) + ".0",
    contact={
        "name": "Danil Fedorov",
        "url": "https://t.me/youngWishes",
        "email": "mysc1@yandex.ru",
    },
)

app.include_router(auth_router, tags=["/auth"], prefix="/auth/jwt")
app.include_router(register_router, tags=["/auth"], prefix="/auth")
app.include_router(users_router, tags=["/users"], prefix="/users")

current_user = fastapi_users.current_user()


@app.get("/protected-route")
async def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.email}"


@app.get("/")
async def index():
    return {"diploma": "started"}
