from http import HTTPStatus
from fastapi import APIRouter, Body, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.core import literals as lit
from app.core import db
from app.crud import meeting_room as mr_crud
from app.schemas import meeting_room as mr_schemas
from app.models import meeting_room as mr_models


router = APIRouter(
    prefix='/meeting_rooms',
    tags=['Meeting Rooms']
)


@router.post(
    '/',
    summary=lit.API_CREATE_MR,
    response_model=mr_schemas.MeetingRoomResponse,
    response_model_exclude_none=True
)
async def create_new_meeting_room(
    new_room: mr_schemas.MeetingRoomCreate = Body(
        mr_schemas.MeetingRoomCreate.Config.schema
    ),
    session: AsyncSession = Depends(db.get_async_session)
) -> mr_models.MeetingRoom:
    """Принимает JSON и создаёт запись в базе.

    ### Args:
    - new_room: JSON с данными.

    ### Raises:
    - HTTPException: Совпадение названий.

    ### Returns:
    - mr_models.MeetingRoom: Объект на основе вновь созданной записи в БД.
    """
    room_id = await mr_crud.get_room_id_by_name(new_room.name, session)

    if room_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=lit.ERR_ROOM_NAME_BUSY % new_room.name
        )
    return await mr_crud.create_meeting_room(new_room, session)


@router.get(
    '/',
    summary=lit.API_GET_ROOMS,
    response_model=list[mr_schemas.MeetingRoomResponse],
    response_model_exclude_none=True
)
async def get_all_meeting_rooms(
    session: AsyncSession = Depends(db.get_async_session)
) -> list[mr_models.MeetingRoom]:

    return await mr_crud.read_all_rooms_from_db(session)
