import sqlalchemy as sql
import sqlalchemy.orm as orm
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from app.core.config import settings


async_engine = create_async_engine(settings.database_url)

async_session = AsyncSession(bind=async_engine)

AsyncSessionLocal = orm.sessionmaker(bind= async_engine,)


class PreBase:

    @orm.declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = sql.Column(sql.Integer(), primary_key=True)


Base = orm.declarative_base(PreBase)
