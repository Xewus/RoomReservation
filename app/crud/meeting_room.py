from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.meeting_room import MeetingRoom
from app.schemas.meeting_room import MeetingRoomCreate, MeetingRoomUpdate

from .base import CRUDBase


class CRUDMeetingRoom(CRUDBase[
    MeetingRoom,
    MeetingRoomCreate,
    MeetingRoomUpdate
]):
    async def get_id_by_name(
        self,
        name: str,
        session: AsyncSession
    ) -> None | int:
        """Получает id комнаты по названию.

        ### Args:
        - name (str): _description_
        - session (AsyncSession): _description_
        """
        return await session.scalar(
            select(MeetingRoom.id).where(MeetingRoom.name == name)
        )


meeting_room_crud = CRUDMeetingRoom(MeetingRoom)
