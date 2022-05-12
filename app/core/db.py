from sqlalchemy import Column, Integer
from sqlalchemy.orm import declarative_base, declared_attr, sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

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

async_engine = create_async_engine(settings.database_url)

AsyncSessionLocal = sessionmaker(bind=async_engine, class_=AsyncSession)
