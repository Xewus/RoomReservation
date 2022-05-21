import sqlalchemy as sa
import fastapi_users_db_sqlalchemy as fa_u_sa

from app.core import db
from app.core import literals as lit


class Reservation(db.Base):
    """`reservation`

    ### Args:
    - db (_type_): _description_
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
        return lit.ROOM_BUSY % (self.start_time, self.end_time)
