from datetime import datetime

from sqlalchemy import func, select
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
    """Класс с дополнительными методами для таблицы `reservation`.

    Родительские методы переопределены для документирования.
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

    async def get(
        self, room_id: int, session: AsyncSession
    ) -> None | Reservation:
        """Получает бронь с указанным id.

        ### Args:
        - room_id (int): id искомой брони.
        - session (AsyncSession): Объект сессии.

        ### Returns:
        - None | Reservation: Запрошенная бронь.
        """
        return await super().get(room_id, session)

    async def create(
        self,
        data: ReservationCreate,
        session: AsyncSession,
        user: None | UserDB = None
    ) -> Reservation:
        """Создаёт новую бронь.

        ### Args:
        - data (ReservationCreate): Данные для создания брони.
        - session (AsyncSession): Объект сессии.
        - user (None | UserDB, optional): Пользователь, создающий бронь.
            Defaults to None.

        ### Returns:
        - Reservation: Вновь созданная бронь.
        """
        return await super().create(data, session, user)

    async def update(
        self,
        reservation: Reservation,
        update_data: ReservationUpdate,
        session: AsyncSession
    ) -> Reservation:
        """Обновление данных указанной брони.

        ### Args:
        - reservation (Reservation): Запрошенная бронь.
        - update_data (ReservationUpdate): Данные для обновления.
        - session (AsyncSession): Объект сессии.

        ### Returns:
        - Reservation: Обновлённая бронь.
        """
        return await super().update(reservation, update_data, session)

    async def remove(
        self,
        reservation: Reservation,
        session: AsyncSession
    ) -> Reservation:
        """Удаляет указанную бронь.

        ### Args:
        - reservation (Reservation): Запрошенная бронь.
        - session (AsyncSession): Объект сессии.

        ### Returns:
        - Reservation: Обновлённая бронь.
            После удаления данные брони всё ещё остаются в сессии.
        """
        return await super().remove(reservation, session)

    async def count_reses_in_time_interval(
        self,
        start_time: datetime,
        end_time: datetime,
        session: AsyncSession
    ) -> list[dict[str, int]]:
        """Возвращает количество броней в указанный период
        времени для каждой комнаты.

        ### Args:
        - start_time (datetime):
            Начало временного периода.
        - end_time (datetime):
            _Окончание временного периода.
        - session (AsyncSession):
            Объект сессии БД.

        ### Returns:
        - list[dict[str, int]]:
            Список в виде [{'room_id': 5}, ...]
        """
        rooms = await session.execute(
            select(
                [Reservation.room_id, func.count(Reservation.room_id)]
                ).where(
                    Reservation.start_time < end_time,
                    Reservation.end_time > start_time
                ).group_by(
                    Reservation.room_id
                )
            )
        return rooms.all()


reservation_crud = CRUDReservation(Reservation)
