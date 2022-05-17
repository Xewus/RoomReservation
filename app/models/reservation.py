import sqlalchemy as sa

from app.core import db


class Reservation(db.Base):
    """`reservation`

    ### Args:
    - db (_type_): _description_
    """
    from_reserve = sa.Column(sa.DateTime)
    to_reserve = sa.Column(sa.DateTime)
    meetingroom_id = sa.Column(sa.Integer, sa.ForeignKey('meetingroom.id'))
