from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.reservation import Reservation
from app.schemas.reservation import ReservationCreate, ReservationUpdate


class CRUDReservation(CRUDBase[
    Reservation,
    ReservationCreate,
    ReservationUpdate
]):
    async def get_reservations_by_time(
        self,
        *,  # все дальнейшие параметры по ключу
        room_id: int,
        start_time: datetime,
        end_time: datetime,
        reservation_id: None | int,
        session: AsyncSession
    ) -> list[Reservation]:
        query = select(Reservation).where(
            Reservation.room_id == room_id,
            Reservation.start_time.between(start_time, end_time) |
            Reservation.end_time.between(start_time, end_time) |
            (Reservation.start_time <= start_time) &
            (Reservation.end_time >= end_time)
        )
        if reservation_id is not None:
            query = query.where(Reservation.id != reservation_id)

        reservations = await session.scalars(query)
        return reservations.all()


reservation_crud = CRUDReservation(Reservation)
