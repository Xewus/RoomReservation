import fastapi as fa
import fastapi_users as fa_u
import fastapi_users.authentication as auth
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import config, db
from app.models import user as model
from app.schemas import user as schema


async def get_user_db(
    session: AsyncSession = fa.Depends(db.get_async_session)
):
    yield SQLAlchemyUserDatabase(schema.UserDB, session, model.UserTable)


# Определяем транспорт - передача токена
# через заголовок HTTP-запроса Authorization: Bearer.
# Указываем URL эндпоинта для получения токена.
bearer_transport = auth.BearerTransport(tokenUrl='auth/jwt/login')


# Определяем стратегию: хранение токена в виде JWT.
def get_jwt_strategy() -> auth.JWTStrategy:
    # В специальный класс из настроек приложения
    # передается секретное слово, используемое для генерации токена.
    # Вторым аргументом передаём время действия токена в секундах.
    return auth.JWTStrategy(
        secret=config.settings.secret, lifetime_seconds=3600
    )


# Создаём объект бэкенда аутентификации с выбранными параметрами.
auth_backend = auth.AuthenticationBackend(
    name='jwt',  # Произвольное имя бэкенда (должно быть уникальным).
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)


# Здесь тоже используются «дженерики».
class UserManager(fa_u.BaseUserManager[schema.UserCreate, schema.UserDB]):
    user_db_model = schema.UserDB
    reset_password_token_secret = config.settings.secret
    verification_token_secret = config.settings.secret

    # Здесь можно описать свои условия валидации пароля.
    # При успешной валидации функция ничего не возвращает.
    # При ошибке валидации - вызывает специальный класс ошибки
    # InvalidPasswordException.
    async def validate_password(
        self,
        password: str,
        user: schema.UserCreate | schema.UserDB,
    ) -> None:
        if len(password) < 8:
            raise fa_u.InvalidPasswordException(
                reason='Password should be at least 8 characters'
            )
        if user.email in password:
            raise fa_u.InvalidPasswordException(
                reason='Password should not contain e-mail'
            )

    # Пример метода для действий после успешной регистрации пользователя.
    async def on_after_register(
            self, user: schema.UserDB, request: None | fa.Request = None
    ):
        # Вместо print здесь можно было бы настроить отправку письма.
        print(f'Пользователь {user.email} был зарегистрирован')


# Корутина, возвращающая объект класса UserManager.
async def get_user_manager(user_db=fa.Depends(get_user_db)):
    yield UserManager(user_db)

fastapi_users = fa_u.FastAPIUsers(
    get_user_manager=get_user_manager,
    auth_backends=[auth_backend],
    user_model=schema.User,
    user_create_model=schema.UserCreate,
    user_update_model=schema.UserUpdate,
    user_db_model=schema.UserDB
)

current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
