import sqlalchemy as sa
import sqlalchemy.orm as orm

from app.core import db


class MeetingRoom(db.Base):
    """ORM-модель для переговорных комнат.

    Назавние в БД - `meetinfroom`

    ## Attrs:
    - name: Название комнаты.
    - description: Описание комнаты.
    - reservation: Связь O2M с таблицей `reservation`
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
