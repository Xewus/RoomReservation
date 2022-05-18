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
        room_id: int,
        start_time: datetime,
        end_time: datetime,
        session: AsyncSession
    ) -> list[Reservation]:
        reservations = await session.scalars(select(Reservation.id).where(
            Reservation.room_id == room_id,
            Reservation.start_time.between(start_time, end_time) |
            Reservation.end_time.between(start_time, end_time) |
            (Reservation.start_time <= start_time) &
            (Reservation.end_time >= end_time)
        ))
        return reservations.all()


reservation_crud = CRUDReservation(Reservation)
