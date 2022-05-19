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
    reservation = await validators.check_reservation_exists(reservation_id, session)
    return await crud.remove(reservation, session)
