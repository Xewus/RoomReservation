from http import HTTPStatus

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import validators
from app.core import db
from app.core import literals as lit
from app.crud.reservation import reservation_crud as crud
from app.models import reservation as model
from app.schemas import reservation as schema

router = APIRouter()


@router.get(
    '/',
    summary=lit.API_GET_RESERVATION,
    response_model=list[schema.ReservationResponse]
)
async def get_all_reservations(
    session: AsyncSession = Depends(db.get_async_session)
) -> list[model.Reservation]:
    return await crud.get_all(session)


@router.post(
    '/',
    summary=lit.API_CREATE_RESERVATION,
    status_code=HTTPStatus.CREATED,
    response_model=schema.ReservationResponse
)
async def create(
    new_reserve: schema.ReservationCreate,
    session: AsyncSession = Depends(db.get_async_session)
) -> model.Reservation:
    await validators.check_meeting_room_exists(new_reserve.room_id, session)
    await validators.check_time_reservation(
        room_id=new_reserve.room_id,
        start_time=new_reserve.start_time,
        end_time=new_reserve.end_time,
        session=session
    )
    return await crud.create(new_reserve, session)


@router.patch(
    '/{reservation_id}',
    summary=lit.API_UPDATE_RESERVATION,
    response_model=schema.ReservationUpdate
)
async def update_reservation(
    reservation_id: int,
    update_data: schema.ReservationUpdate,
    session: AsyncSession = Depends(db.get_async_session)
):
    reservation = await validators.check_reservation_exists(
        reservation_id,
        session
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
    summary=lit.API_DELETE_RESERVATION,
    status_code=HTTPStatus.OK,
    response_model=schema.ReservationResponse
)
async def delete_reservation(
    reservation_id: int,
    session: AsyncSession = Depends(db.get_async_session)
) -> model.Reservation:
    reservation = await validators.check_reservation_exists(
        reservation_id,
        session
    )
    return await crud.remove(reservation, session)


@router.get(
    '/{room_id}/reservations',
    summary=lit.API_BUSY_PERIODS,
    response_model=list[schema.ReservationBase]
)
async def get_reservations_for_room(
    room_id: int,
    session: AsyncSession = Depends(db.get_async_session)
) -> list[model.Reservation]:
    await validators.check_meeting_room_exists(room_id, session)
    return await crud.get_busy_times_for_room(room_id, session)
