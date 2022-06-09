import sqlalchemy as sa
import fastapi_users_db_sqlalchemy as fa_u_sa

from app.core import db
from app.services import constants as const


class Reservation(db.Base):
    """`reservation`

    ### Attrs:
    - start_time (DateTime): Начало времени брони.
    - end_time (DateTime): Конец времени брони.
    - room_id (ForeignKey):
        Ссылка на бронируему комнату в таблице ('meetingroom.id').
    user_id (ForeignKey)Ж Ссылка на пользователя, создавшего бронь ('user.id').
    """
    start_time = sa.Column(
        sa.DateTime
    )
    end_time = sa.Column(
        sa.DateTime
    )
    room_id = sa.Column(
        sa.Integer,
        sa.ForeignKey('meetingroom.id')
    )
    user_id = sa.Column(
        fa_u_sa.GUID,
        sa.ForeignKey('user.id')
    )

    def __repr__(self) -> str:
        return const.ROOM_BUSY % (self.start_time, self.end_time)
