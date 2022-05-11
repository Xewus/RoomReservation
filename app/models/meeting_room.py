import sqlalchemy as sql

from app.core.db import Base


class MettingRoom(Base):
    name = sql.Column(
        sql.String(100),
        unique=True,
        nullable=False
    )
