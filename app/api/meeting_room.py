from http.client import HTTPException
from fastapi import APIRouter, Body, HTTPException

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
    room_id = await mr_crud.get_room_id_by_name(new_room.name)
    if room_id is not None:
        raise HTTPException(
            status_code=422,
            detail='Переговорка с таким именем уже существует!'
        )
    room = await mr_crud.create_meeting_room(new_room)
    return room
