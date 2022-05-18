import sqlalchemy as sa

from app.core import db
from app.core import literals as lit


class Reservation(db.Base):
    """`reservation`

    ### Args:
    - db (_type_): _description_
    """
    start_time = sa.Column(sa.DateTime)
    end_time = sa.Column(sa.DateTime)
    room_id = sa.Column(sa.Integer, sa.ForeignKey('meetingroom.id'))

    def __repr__(self) -> str:
        return lit.ROOM_BUSY % self.start_time, self.end_time
