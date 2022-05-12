from sqlalchemy import select

from app.core import db
from app.models import meeting_room as mr_models
from app.schemas import meeting_room as mr_schemas


async def create_meeting_room(
    new_room: mr_schemas.MeetingRoomCreate
) -> mr_models.MeetingRoom:
    """Создаёт и записывает в БД объект MeetingRoom.

    ### Args:
    - new_room (mr_schemas.MeetingRoomCreate): Данные для нового объекта.

    ### Returns:
    - mr_models.MeetingRoom: Вновь созданный объект.
    """
    data = new_room.dict()
    room = mr_models.MeetingRoom(**data)

    async with db.AsyncSessionLocal() as session:
        session.add(room)
        await session.commit()
        await session.refresh(room)

    return room


async def get_room_id_by_name(name: str) -> int | None:
    """Получает id объекта по названию.

    ### Args:
    - name (str): Название искогомого обэекта.

    ### Returns:
    - int | None: id объекта, если найден.
    """
    async with db.AsyncSessionLocal() as session:
        room_id = await session.execute(
            select(mr_models.MeetingRoom.id).where(
                mr_models.MeetingRoom.name == name
            )
        )
        room_id = room_id.scalar()
    return room_id
