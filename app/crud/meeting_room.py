from .base import CRUDBase

from app.models.meeting_room import MeetingRoom
from app.schemas import meeting_room as mr_schemas

meeting_room_crud = CRUDBase[
    MeetingRoom, 
    mr_schemas.MeetingRoomCreate, 
    mr_schemas.MeetingRoomUpdate
](MeetingRoom)
