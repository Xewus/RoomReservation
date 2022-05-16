from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import meeting_room as mr_models
from app.schemas import meeting_room as mr_schemas


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


async def read_all_rooms_from_db(
    session: AsyncSession
) -> list[mr_models.MeetingRoom]:
    """Считывает из БД объекты MeetingRoom и возвращает их.
    """
    rooms = await session.execute(select(mr_models.MeetingRoom))
    return rooms.scalars().all()
