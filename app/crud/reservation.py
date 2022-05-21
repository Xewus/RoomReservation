from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.reservation import Reservation
from app.schemas.reservation import ReservationCreate, ReservationUpdate
from app.schemas.user import UserDB


class CRUDReservation(CRUDBase[
    Reservation,
    ReservationCreate,
    ReservationUpdate
]):
    """Класс с дополнительными методами для таблицы `Reservation`.
    """
    async def get_reservations_by_time(
        self,
        *,  # все дальнейшие параметры по ключу
        room_id: int,
        start_time: datetime,
        end_time: datetime,
        reservation_id: None | int = None,
        session: AsyncSession
    ) -> list[Reservation]:
        """Получает список броней попадающих в указанный период времени.

        ### Args:
        - start_time (datetime): Начала периода.
        - end_time (datetime): Конец периода.
        - session (AsyncSession): Объект сессии.
        - reservation_id (None | int): Бронь, время которой следует исключить
          из списка. Defaults to None.

        ### Returns:
        - list[Reservation]: Список броней.
        """
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

    async def get_busy_times_for_room(
        self,
        room_id: int,
        session: AsyncSession
    ) -> list[Reservation]:
        """Список броней для указанной комнаты.

        Список начинается с актуального времени.

        ### Args:
        - room_id (int): Id комнаты.
        - session (AsyncSession): Объект сессии.

        ### Returns:
        - list[Reservation]: Список броней.
        """
        reservations = await session.scalars(
            select(
                Reservation
            ).where(
                Reservation.room_id == room_id,
                Reservation.end_time > datetime.now()
            )
        )
        return reservations.all()

    async def get_reservation_by_user(
        self,
        user: UserDB,
        session: AsyncSession
    ) -> list[Reservation]:
        """
        Список броней указанного пользователя.

        ### Args:
        - user (UserDB): Пользователь.
        - session (AsyncSession): Объект сессии.

        ### Returns:
        - list[Reservation]: Список броней.
        """
        reservations = await session.scalars(
            select(
                Reservation
            ).where(
                Reservation.user_id == user.id
            )
        )
        return reservations.all()


reservation_crud = CRUDReservation(Reservation)
