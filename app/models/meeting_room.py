import sqlalchemy as sa

from app.core import db


class MeetingRoom(db.Base):
    name = sa.Column(
        sa.String(100),
        unique=True,
        nullable=False
    )
    description = sa.Column(
        sa.Text()
    )
