from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.meeting_room import MeetingRoom
from app.schemas.meeting_room import MeetingRoomCreate, MeetingRoomUpdate
from app.schemas.user import UserDB

from .base import CRUDBase


class CRUDMeetingRoom(CRUDBase[
    MeetingRoom,
    MeetingRoomCreate,
    MeetingRoomUpdate
]):
    """Класс с дополнительными методами для таблицы `meetingroom`.

    Родительские методы переопределены для документирования.
    """
    async def get_id_by_name(
        self,
        name: str,
        session: AsyncSession
    ) -> None | int:
        """Получает id комнаты по названию.

        ### Args:
        - name (str): Название комнаты.
        - session (AsyncSession): Объект сессии.

        ### Returns:
        - None | int: id запрошенной комнаты.
        """
        room_id = await session.scalar(
            select(MeetingRoom.id).where(MeetingRoom.name == name)
        )
        return room_id

    async def get(
        self, obj_id: int, session: AsyncSession
    ) -> None | MeetingRoom:
        """Получает комнату по id.

        ### Args:
        - obj_id (int): id омнаты.
        - session (AsyncSession): Объект сессии.

        ### Returns:
        - None | MeetingRoom: Запрошенная комната.
        """
        return await super().get(obj_id, session)

    async def get_all(
        self, session: AsyncSession
    ) -> list[MeetingRoom]:
        """Получает список всех комнат.

        ### Args:
        - session (AsyncSession): Объект сессии.

        ### Returns:
        - list[MeetingRoom]: Список всех комнат.
        """
        return await super().get_all(session)

    async def create(
        self,
        data: MeetingRoomCreate,
        session: AsyncSession,
        user: None | UserDB = None
    ) -> MeetingRoom:
        """Создаёт запись в БД с данными новой комнаты.

        ### Args:
        - data (MeetingRoomCreate): Данные новой комнаты.
        - session (AsyncSession): Объект сессии.
        - user (None | UserDB, optional):
            Пользователь, создающий новую комнату.
            Defaults to None.

        ### Returns:
        - MeetingRoom: Вновь созданная комната.
        """
        return await super().create(data, session, user)

    async def update(
        self,
        room: MeetingRoom,
        update_data: MeetingRoomUpdate,
        session: AsyncSession
    ) -> MeetingRoom:
        """Обновляет данные указанной комнаты.

        ### Args:
        - room (MeetingRoom): Запрошеннай комната.
        - update_data (MeetingRoomUpdate): Схема данных для обновления.
        - session (AsyncSession): Объект сессии.

        ### Returns:
        - model.MeetingRoom: Обновлённая комната.
        """
        return await super().update(room, update_data, session)

    async def remove(
        self, room: MeetingRoom, session: AsyncSession
    ) -> MeetingRoom:
        """Удаляет указанную комнату.

        ### Args:
        - room (MeetingRoom): Запрошенная комната.
        - session (AsyncSession):Объект сессии.
        ### Returns:
        - MeetingRoom: Удалённая комната.
            После удаления данные комнаты всё ещё остаются в сессии.
        """
        return await super().remove(room, session)


meeting_room_crud = CRUDMeetingRoom(MeetingRoom)
