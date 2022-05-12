from fastapi import APIRouter, Body

from app.core import literals as lit
from app.crud import meeting_room as mr_crud
from app.schemas import meeting_room as mr_schemas
from app.models import meeting_room as mr_models


router = APIRouter()


@router.post('/meeting_rooms/', summary=lit.API_CREATE_MR)
async def create_new_meeting_room(
    new_room: mr_schemas.MeetingRoomCreate = Body(
        ...,
        example=mr_schemas.MeetingRoomCreate.Config.schema['example']
    )
) -> mr_models.MeetingRoom:
    room = await mr_crud.create_meeting_room(new_room)
    return room
