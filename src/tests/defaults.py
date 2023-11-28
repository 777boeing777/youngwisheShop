from src.core.config import get_settings

settings = get_settings(db_only=True)

TEST_DB_NAME = "test_db"

SQLALCHEMY_DATABASE_TEST_URI = (
    f"{settings.POSTGRES_DRIVER}://"
    f"{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}"
    f"@{settings.POSTGRES_HOST}/{TEST_DB_NAME}"
)

HOST_URL = "http://0.0.0.0:8000/"

TEST_USER_EMAIL = "test@example.com"

TEST_USER_FIRST_NAME = "test_first_name"

TEST_USER_LAST_NAME = "test_user_last_name"

TEST_USER_MIDDLE_NAME = "test_user_middle_name"

TEST_USER_PASSWORD = "test_user_password"
