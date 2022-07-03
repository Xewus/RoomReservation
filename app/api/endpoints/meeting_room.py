from http import HTTPStatus

from fastapi import APIRouter, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import validators
from app.core import db, user
from app.crud.meeting_room import meeting_room_crud as crud
from app.models import meeting_room as model
from app.services import constants as const
from app.schemas import meeting_room as schema

router = APIRouter()


@router.get(
    '/',
    summary=const.API_GET_MEET_ROOMS,
    response_model=list[schema.MeetingRoomResponse],
    response_model_exclude_none=True
)
async def get_all_meeting_rooms(
    session: AsyncSession = Depends(db.get_async_session)
) -> list[model.MeetingRoom]:
    """Получает список всех комнат.

    ### Args:
    - session (AsyncSession): Объект сессии.

    ### Returns:
    - list[model.MeetingRoom]: Список всех комнат.
    """
    return await crud.get_all(session)


@router.post(
    '/',
    summary=const.API_CREATE_MEET_ROOM,
    status_code=HTTPStatus.CREATED,
    response_model=schema.MeetingRoomResponse,
    response_model_exclude_none=True,
    dependencies=[Depends(user.current_superuser)]
)
async def create_new_meeting_room(
    new_room: schema.MeetingRoomCreate = Body(
        schema.MeetingRoomCreate.Config.schema
    ),
    session: AsyncSession = Depends(db.get_async_session)
) -> model.MeetingRoom:
    """Создаёт новую комнату.

    Только для суперюзеров.

    ### Args:
    - new_room: Данные новой комнаты.
    - session (AsyncSession): Объект сессии.

    ### Raises:
    - HTTPException: Совпадение названий.

    ### Returns:
    - model.MeetingRoom: Вновь созданная комната.
    """
    await validators.check_name_exist(new_room.name, session)

    return await crud.create(new_room, session)


@router.patch(
    '/{room_id}',
    summary=const.API_UPDATE_MEET_ROOM,
    status_code=HTTPStatus.ACCEPTED,
    response_model=schema.MeetingRoomUpdate,
    response_model_exclude_none=True,
    dependencies=[Depends(user.current_superuser)],
)
async def partially_update_meeting_room(
    room_id: int,
    update_data: schema.MeetingRoomUpdate,
    session: AsyncSession = Depends(db.get_async_session)
) -> model.MeetingRoom:
    """Обновление данных указанной комнаты.

    Только для суперюзеров.

    ### Args:
    - room_id (int): id запрошенной комнаты.
    - update_data (schema.MeetingRoomUpdate): Схема данных для обновления.
    - session (AsyncSession): Объект сессии.

    ### Returns:
    - model.MeetingRoom: Обновлённая комната.
    """
    room = await validators.check_meeting_room_exists(room_id, session)

    if update_data.name is not None and update_data.name != room.name:
        await validators.check_name_exist(update_data.name, session)

    return await crud.update(room, update_data, session)


@router.delete(
    '/{room_id}',
    summary=const.API_DELETE_MEET_ROOM,
    status_code=HTTPStatus.OK,
    response_model=schema.MeetingRoomUpdate,
    response_model_exclude_none=True,
    dependencies=[Depends(user.current_superuser)],
)
async def remove_meeting_room(
    room_id: int,
    session: AsyncSession = Depends(db.get_async_session)
) -> model.MeetingRoom:
    """Удаляет указанную комнату.

    ### Args:
    - room_id (int): _description_
    - session (AsyncSession, optional): Объект сессии.

    ### Returns:
        - model.MeetingRoom: Удалённая комната.
            После удаления данные комнаты всё ещё остаются в сессии.
    """
    room = await validators.check_meeting_room_exists(room_id, session)

    return await crud.remove(room, session)
