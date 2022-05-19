from http import HTTPStatus

from fastapi import APIRouter, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import validators
from app.core import db
from app.core import literals as lit
from app.crud.meeting_room import meeting_room_crud as crud
from app.models import meeting_room as model
from app.schemas import meeting_room as schema

router = APIRouter()


@router.get(
    '/',
    summary=lit.API_GET_MEET_ROOMS,
    response_model=list[schema.MeetingRoomResponse],
    response_model_exclude_none=True
)
async def get_all_meeting_rooms(
    session: AsyncSession = Depends(db.get_async_session)
) -> list[model.MeetingRoom]:
    return await crud.get_all(session)


@router.post(
    '/',
    summary=lit.API_CREATE_MEET_ROOM,
    status_code=HTTPStatus.CREATED,
    response_model=schema.MeetingRoomResponse,
    response_model_exclude_none=True
)
async def create_new_meeting_room(
    new_room: schema.MeetingRoomCreate = Body(
        schema.MeetingRoomCreate.Config.schema
    ),
    session: AsyncSession = Depends(db.get_async_session)
) -> model.MeetingRoom:
    """Принимает JSON и создаёт запись в базе.

    ### Args:
    - new_room: JSON с данными.

    ### Raises:
    - HTTPException: Совпадение названий.

    ### Returns:
    - model.MeetingRoom: Объект на основе вновь созданной записи в БД.
    """
    await validators.check_name_exist(new_room.name, session)

    return await crud.create(new_room, session)


@router.patch(
    '/{room_id}',
    summary=lit.API_UPDATE_MEET_ROOM,
    status_code=HTTPStatus.ACCEPTED,
    response_model=schema.MeetingRoomUpdate,
    response_model_exclude_none=True
)
async def partially_update_meeting_room(
    room_id: int,
    update_data: schema.MeetingRoomUpdate,
    session: AsyncSession = Depends(db.get_async_session)
):
    room = await validators.check_meeting_room_exists(room_id, session)

    if update_data.name is not None and update_data.name != room.name:
        await validators.check_name_exist(update_data.name, session)

    return await crud.update(room, update_data, session)


@router.delete(
    '/{room_id}',
    summary=lit.API_DELETE_MEET_ROOM,
    status_code=HTTPStatus.OK,
    response_model=schema.MeetingRoomUpdate,
    response_model_exclude_none=True
)
async def remove_meeting_room(
    room_id: int,
    session: AsyncSession = Depends(db.get_async_session)
):
    room = await validators.check_meeting_room_exists(room_id, session)

    return await crud.remove(room, session)
