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


@router.get(
    '/',
    summary=lit.API_GET_MEET_ROOMS,
    response_model=list[mr_schemas.MeetingRoomResponse],
    response_model_exclude_none=True
)
async def get_all_meeting_rooms(
    session: AsyncSession = Depends(db.get_async_session)
) -> list[mr_models.MeetingRoom]:

    return await mr_crud.read_all_rooms_from_db(session)


@router.post(
    '/',
    summary=lit.API_CREATE_MEET_ROOM,
    status_code=HTTPStatus.CREATED,
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
    if await mr_crud.value_in_db_exist(
        mr_models.MeetingRoom,
        'name',
        new_room.name,
        session
    ):
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=lit.ERR_ROOM_NAME_BUSY % new_room.name
        )

    return await mr_crud.create_meeting_room(new_room, session)


@router.patch(
    '/',
    summary=lit.API_UPDATE_MEET_ROOM,
    status_code=HTTPStatus.ACCEPTED,
    response_model=mr_schemas.MeetingRoomUpdate,
    response_model_exclude_none=True
)
async def partially_update_meeting_room(
    room_id: int,
    update_data: mr_schemas.MeetingRoomUpdate,
    session: AsyncSession = Depends(db.get_async_session)
):
    room = await mr_crud.get_meeting_room_by_id(room_id, session)
    if room is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=lit.ERR_ROOM_NOT_FOUND_ID
        )
    if update_data.name is not None and update_data.name != room.name:
        if await mr_crud.value_in_db_exist(
            table=mr_models.MeetingRoom,
            table_field='name',
            value=update_data.name,
            session=session
        ):
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail=lit.ERR_ROOM_NAME_BUSY % update_data.name
            )
    return await mr_crud.update_meeting_room(room, update_data, session)
