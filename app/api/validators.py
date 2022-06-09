from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.meeting_room import meeting_room_crud as mr_crud
from app.crud.reservation import reservation_crud as rsr_crud
from app.models.meeting_room import MeetingRoom
from app.models.reservation import Reservation
from app.services import constants as const
from app.schemas.user import UserDB


async def check_name_exist(
        room_name: str,
        session: AsyncSession,
) -> None:
    """Проверяет наличие комнаты с данным названием.

    ### Args:
    - room_name (str): Название комнаты.
    - session (AsyncSession): Объект сессии.

    ### Raises:
    - HTTPException: Такое название уже занято.

    ### Returns:
    - None
    """
    if await mr_crud.get_id_by_name(room_name, session) is not None:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=const.ERR_ROOM_NAME_BUSY % room_name
        )


async def check_meeting_room_exists(
        room_id: int,
        session: AsyncSession,
) -> MeetingRoom:
    """Проверяет наличие переговорной комнаты с указанным id.

    ### Args:
    - room_id (int): id комнаты.
    - session (AsyncSession): Объект сессии.

    ### Raises:
    - HTTPException: Комната с данным id не найдена.

    ### Returns:
    - MeetingRoom: Запрошенная комната.
    """
    meeting_room = await mr_crud.get(room_id, session)
    if meeting_room is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=const.ERR_ROOM_NOT_FOUND_ID % room_id
        )
    return meeting_room


async def check_time_reservation(**kwargs) -> None:
    """Проверяет, свобден ли указанный период времени для запрошенной комнаты.

    ### Raises:
    - HTTPException: Данный период времени пересекается с другими.

    ### Returns:
    - None
    """
    reservations = await rsr_crud.get_reservations_by_time(**kwargs)
    if reservations:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=const.ERR_TIME_RESERVATION % (kwargs['room_id'], reservations)

        )


async def check_reservation_exists(
    reservation_id: int,
    session: AsyncSession,
    user: None | UserDB = None,
) -> Reservation:
    """Проверяет наличие комнаты с указанным id.

    Опциональный параметр `user` ограничивает доступ.

    ### Args:
    - reservation_id (int): id искомой брони.
    - session (AsyncSession): Объект сессии.
    - user (None | UserDB, optional): Если передан, то должен быть
        суперпользователем или создателем брони, иначе доступ запрещён.
        Defaults to None.

    ### Raises:
    - HTTPException: Бронь с указанным id не найдена.
    - HTTPException: Поьзователь не суперюзер и не создатель брони.

    ### Returns:
    - Reservation: Запрошенная бронь.
    """
    reservation = await rsr_crud.get(reservation_id, session)
    if reservation is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=const.ERR_RESERVATION_NOT_FOUND_ID % reservation_id
        )
    if not user.is_superuser and reservation.user_id != user.id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail=const.ERR_NOT_OWNER
        )
    return reservation
