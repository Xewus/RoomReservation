from .base import CRUDBase
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.meeting_room import MeetingRoom
from app.schemas import meeting_room as mr_schemas


meeting_room_crud = CRUDBase(MeetingRoom)
