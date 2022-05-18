from sqlalchemy import Column, Integer
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base, declared_attr, sessionmaker

from app.core.config import settings


class PreBase:
    """Подготовительный класс для ORM-моделей.

    Устанавливает для наследников название таблиц в формате lowercase
    и автоматическое добавление столбца id.

    ### Attrs:
    - id: Столбец для первичного ключа.
    """

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer(), primary_key=True)


Base = declarative_base(cls=PreBase)

async_engine = create_async_engine(
    settings.database_url,
    echo=settings.echo
)

AsyncSessionLocal = sessionmaker(bind=async_engine, class_=AsyncSession)


async def get_async_session():
    async with AsyncSessionLocal() as async_session:
        yield async_session
