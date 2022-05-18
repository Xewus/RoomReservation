from http import HTTPStatus
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.meeting_room import meeting_room_crud as mr_crud
from app.models.meeting_room import MeetingRoom
from app.core import literals as lit


async def check_name_exist(
        room_name: str,
        session: AsyncSession,
) -> None:
    if await mr_crud.get_id_by_name(room_name, session) is not None:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=lit.ERR_ROOM_NAME_BUSY % room_name
        )


async def check_meeting_room_exists(
        room_id: int,
        session: AsyncSession,
) -> MeetingRoom:
    meeting_room = await mr_crud.get(room_id, session)
    if meeting_room is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=lit.ERR_ROOM_NOT_FOUND_ID % room_id
        )
    return meeting_room
