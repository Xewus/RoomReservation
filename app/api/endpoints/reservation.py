from http import HTTPStatus

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import validators
from app.core import db
from app.core import literals as lit
from app.crud.reservation import reservation_crud as rsr_crud
from app.models import reservation as rsr_model
from app.schemas import reservation as rsr_schema

router = APIRouter()


@router.post(
    '/',
    summary=lit.API_CREATE_RESERVE,
    status_code=HTTPStatus.CREATED,
    response_model=rsr_schema.ReservationResponse
    )
async def create(
    new_reserve: rsr_schema.ReservationCreate,
    session: AsyncSession = Depends(db.get_async_session)
) -> rsr_model.Reservation:
    await validators.check_meeting_room_exists(new_reserve.room_id, session)
    await validators.check_time_reservation(
        room_id=new_reserve.room_id,
        start_time=new_reserve.start_time,
        end_time=new_reserve.end_time,
        session=session
    )
    return await rsr_crud.create(new_reserve, session)
