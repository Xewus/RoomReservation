import sqlalchemy as sa
import sqlalchemy.orm as orm
import sqlalchemy.ext.asyncio as sa_async

from app.core.config import settings


class PreBase:

    @orm.declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = sa.Column(sa.Integer(), primary_key=True)


Base = orm.declarative_base(cls=PreBase)

async_engine = sa_async.create_async_engine(settings.database_url)

async_session = sa_async.AsyncSession(bind=async_engine)

AsyncSessionLocal = orm.sessionmaker(bind=async_engine,)
