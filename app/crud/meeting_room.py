from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import meeting_room as mr_models
from app.schemas import meeting_room as mr_schemas
from app.core.db import Base


async def get_meeting_room_by_id(
    room_id: int,
    session: AsyncSession
) -> None | mr_models.MeetingRoom:
    """Находит в БД объект `MeetingRoom` по id.

    ### Args:
    - room_id (int): _description_
    - session (AsyncSession): _description_

    ### Returns:
    - None | mr_models.mr_models.MeetingRoom: _description_
    """
    return await session.scalar(
        select(
            mr_models.MeetingRoom
        ).where(
            mr_models.MeetingRoom.id == room_id
        )
    )


async def get_room_id_by_name(
    name: str,
    session: AsyncSession
) -> None | int:
    """Получает id объекта по названию.

    ### Args:
    - name (str): Название искогомого обэекта.

    ### Returns:
    - int | None: id объекта, если найден.
    """
    return await session.scalar(
            select(mr_models.MeetingRoom.id).where(
                mr_models.MeetingRoom.name == name
            )
        )


async def value_in_db_exist(
    table: Base,
    table_field: str,
    value: str,
    session: AsyncSession,
    id: None | int = None,
) -> bool:
    """Проверяет наличие значения в запрошенном поле таблицы.

    ### Args:
    - table (Base): Запрашиваемая таблица.
    - table_field (str): Запрашиваемое поле в таблице.
    - value (str): Проверяемое значение.
    - session (AsyncSession): Сеесия соединения с БД.
    - id (None | int, optional): id объекта. Defaults to None.

    ### Returns:
    - bool: Существует или нет запрошенное значение в запрошенном поле.
    """
    table_field = getattr(table, table_field)
    if id is not None:
        table_id = getattr(table, 'id')
        query = select(table_field).where(
            table_field == value, table_id != id
        ).limit(1)
    else:
        query = select(table_field).where(table_field == value).limit(1)
    return bool(await session.scalar(query))


async def read_all_rooms_from_db(
    session: AsyncSession
) -> list[mr_models.MeetingRoom]:
    """Считывает из БД объекты MeetingRoom и возвращает их.
    """
    rooms = await session.execute(select(mr_models.MeetingRoom))
    return rooms.scalars().all()


async def create_meeting_room(
    new_room: mr_schemas.MeetingRoomCreate,
    session: AsyncSession,
) -> mr_models.MeetingRoom:
    """Создаёт и записывает в БД объект MeetingRoom.

    ### Args:
    - new_room (mr_schemas.MeetingRoomCreate): Данные для нового объекта.

    ### Returns:
    - mr_models.MeetingRoom: Вновь созданный объект.
    """
    data = new_room.dict()
    room = mr_models.MeetingRoom(**data)

    session.add(room)
    await session.commit()
    await session.refresh(room)

    return room


async def update_meeting_room(
    room: mr_models.MeetingRoom,
    update_data: mr_schemas.MeetingRoomUpdate,
    session: AsyncSession
) -> mr_models.MeetingRoom:
    """Обновляет данные комнаты

    ### Args:
    - room_id (int): _description_
    - update_data (mr_schemas.MeetingRoomUpdate): _description_
    - session (AsyncSession): _description_

    ### Returns:
    - None | mr_models.MeetingRoom: _description_
    """
    for field, value in update_data.dict(exclude_unset=True).items():
        if getattr(room, field):
            setattr(room, field, value)

    session.add(room)
    await session.commit()
    await session.refresh(room)

    return room


async def delete_meeting_room(
    room: mr_models.MeetingRoom,
    session: AsyncSession
):
    """Удаление комнаты.

    ### Args:
    - room (mr_models.MeetingRoom): _description_
    - session (AsyncSession): _description_

    ### Returns:
    - _type_: _description_
    """
    await session.delete(room)
    await session.commit()
    return room
