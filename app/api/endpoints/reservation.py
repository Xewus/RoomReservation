from http import HTTPStatus

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import validators
from app.core import db
from app.core import user
from app.crud.reservation import reservation_crud as crud
from app.models import reservation as model
from app.services import constants as const
from app.schemas import reservation as rsr_schema
from app.schemas import user as user_schema

router = APIRouter()


@router.get(
    '/',
    summary=const.API_GET_RESERVATION,
    response_model=list[rsr_schema.ReservationResponse],
    dependencies=[Depends(user.current_superuser)]
)
async def get_all_reservations(
    session: AsyncSession = Depends(db.get_async_session)
) -> list[model.Reservation]:
    """Только для суперюзеров. Список всех броней.
    """
    return await crud.get_all(session)


@router.post(
    '/',
    summary=const.API_CREATE_RESERVATION,
    status_code=HTTPStatus.CREATED,
    response_model=rsr_schema.ReservationResponse
)
async def create(
    new_reserve: rsr_schema.ReservationCreate,
    session: AsyncSession = Depends(db.get_async_session),
    current_user: user_schema.UserDB = Depends(user.current_user)
) -> model.Reservation:
    """Создаёт новую бронь.

    ### Args:
    - new_reserve (rsr_schema.ReservationCreate): Данные для новой брони.
    - session (AsyncSession): Объект сессии.
    - current_user (user_schema.UserDB, optional):
        Пользователь, создавший бронь.
        Defaults to Depends(user.current_user).

    ### Returns:
    - model.Reservation: Вновь созданная бронь.
    """
    await validators.check_meeting_room_exists(new_reserve.room_id, session)
    await validators.check_time_reservation(
        room_id=new_reserve.room_id,
        start_time=new_reserve.start_time,
        end_time=new_reserve.end_time,
        session=session
    )
    return await crud.create(new_reserve, session, current_user)


@router.patch(
    '/{reservation_id}',
    summary=const.API_UPDATE_RESERVATION,
    response_model=rsr_schema.ReservationResponse
)
async def update_reservation(
    reservation_id: int,
    update_data: rsr_schema.ReservationUpdate,
    session: AsyncSession = Depends(db.get_async_session),
    current_user: user_schema.UserDB = Depends(user.current_user)
) -> model.Reservation:
    """Обновление данных указанной брони.

    Допуск у суперюзера либо у пользователя, создавшего эту бронь.

    ### Args:
    - reservation_id (int): id обновляемой брони.
    - update_data (rsr_schema.ReservationUpdate): Данные для обновления.
    - session (AsyncSession, optional): Объект сессии.
    - current_user (user_schema.UserDB, optional):
        Пользователь, обновляющий бронь.
        Defaults to Depends(user.current_user).

    ### Returns:
    - model.Reservation: Вновь созданная бронь.
    """
    reservation = await validators.check_reservation_exists(
        reservation_id,
        session,
        current_user
    )
    await validators.check_time_reservation(
        **update_data.dict(),
        reservation_id=reservation_id,
        room_id=reservation.room_id,
        session=session
    )
    return await crud.update(
        obj=reservation,
        update_data=update_data,
        session=session
    )


@router.delete(
    '/{reservation_id}',
    summary=const.API_DELETE_RESERVATION,
    status_code=HTTPStatus.OK,
    response_model=rsr_schema.ReservationResponse
)
async def delete_reservation(
    reservation_id: int,
    session: AsyncSession = Depends(db.get_async_session),
    current_user: user_schema.UserDB = Depends(user.current_user)
) -> model.Reservation:
    """Удаляет указанную бронь.

    Допуск у суперюзера либо у пользователя, создавшего эту бронь.

    ### Args:
    - reservation_id (int): id удаляемой брони.
    - session (AsyncSession, optional): Объект сессии.
    - current_user (user_schema.UserDB, optional):
        Пользователь, удаляющий бронь.
        Defaults to Depends(user.current_user).

    ### Returns:
    - Обновлённая бронь.
        После удаления данные брони всё ещё остаются в сессии.
        """
    reservation = await validators.check_reservation_exists(
        reservation_id,
        session,
        current_user
    )
    return await crud.remove(reservation, session)


@router.get(
    '/{room_id}/reservations',
    summary=const.API_BUSY_PERIODS,
    response_model=list[rsr_schema.ReservationBase]
)
async def get_reservations_for_room(
    room_id: int,
    session: AsyncSession = Depends(db.get_async_session)
) -> list[model.Reservation]:
    """Список броней для указанной комнаты.

    Список начинается с актуального времени.


    ### Args:
        - room_id (int): Id комнаты.
        - session (AsyncSession): Объект сессии.

    ### Returns:
    - list[model.Reservation]: Список броней.
    """
    await validators.check_meeting_room_exists(room_id, session)
    return await crud.get_busy_times_for_room(room_id, session)


@router.get(
    '/my_reservations',
    response_model=list[rsr_schema.ReservationResponse],
    response_model_exclude={'user_id'}
)
async def get_my_reservations(
    user: user_schema.UserDB = Depends(user.current_user),
    session: AsyncSession = Depends(db.get_async_session)
) -> list[model.Reservation]:
    """Возвращает список броней запращивающего пользователя.

    ### Args:
    - user (user_schema.UserDB): Пользователь, запрашивающий свои брони.
    - session (AsyncSession): Объект сессии.

    ### Returns:
    - list[model.Reservation]: Список броней.
    """
    return await crud.get_reservation_by_user(
        user=user,
        session=session
    )
