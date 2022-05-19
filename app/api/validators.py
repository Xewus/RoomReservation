from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import literals as lit
from app.crud.meeting_room import meeting_room_crud as mr_crud
from app.crud.reservation import reservation_crud as rsr_crud
from app.models.meeting_room import MeetingRoom
from app.models.reservation import Reservation


async def check_name_exist(
        room_name: str,
        session: AsyncSession,
) -> None:
    """Проверяет наличие переговорной комнаты с данным названием.

    ### Args:
    - room_name (str): _description_
    - session (AsyncSession): _description_

    ### Raises:
    - HTTPException: _description_
    """
    if await mr_crud.get_id_by_name(room_name, session) is not None:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=lit.ERR_ROOM_NAME_BUSY % room_name
        )


async def check_meeting_room_exists(
        room_id: int,
        session: AsyncSession,
) -> MeetingRoom:
    """Проверяет наличие переговорной комнаты с указанным id.

    ### Args:
    - room_id (int): _description_
    - session (AsyncSession): _description_

    ### Raises:
    - HTTPException: _description_

    ### Returns:
    - MeetingRoom: _description_
    """
    meeting_room = await mr_crud.get(room_id, session)
    if meeting_room is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=lit.ERR_ROOM_NOT_FOUND_ID % room_id
        )
    return meeting_room


async def check_time_reservation(**kwargs) -> None:
    reservations = await rsr_crud.get_reservations_by_time(**kwargs)
    if reservations:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=lit.ERR_TIME_RESERVATION % reservations

        )


async def check_reservation_exists(
    reservation_id: int,
    session: AsyncSession
) -> Reservation:
    reservation = await rsr_crud.get(reservation_id, session)
    if reservation is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=lit.ERR_RESERVATION_NOT_FOUND_ID % reservation_id
        )
    return reservation
