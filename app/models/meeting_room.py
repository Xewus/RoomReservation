import sqlalchemy as sa
import sqlalchemy.orm as orm

from app.core import db


class MeetingRoom(db.Base):
    """ORM-модель для переговорных комнат.

    `meetinfroom`

    ## Attrs:
    - name: Название комнаты.
    - description: Описание комнаты.
    """
    name = sa.Column(
        sa.String(100),
        unique=True,
        nullable=False
    )
    description = sa.Column(
        sa.Text()
    )
    reservation = orm.relationship(
        'Reservation',
        cascade='delete'
    )
