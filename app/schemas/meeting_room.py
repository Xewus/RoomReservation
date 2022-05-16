from pydantic import BaseModel, Field


class MeetingRoomBase(BaseModel):
    """ Базовый класс-схема для MeetingRoom.
    """
    name: str = Field(
        ...,
        title="Название комнаты",
        min_length=1,
        max_length=100
    )
    description: None | str = Field(
        None,
        title="Описание комнаты"
    )


class MeetingRoomCreate(MeetingRoomBase):
    """"Схема для создания новых MeetingRoom."
    """

    class Config:
        orm_mode = True
        title = "Схема для создания новых MeetingRoom"
        schema = {
                'name': 'Главная переговорка',
                'description': 'Очень большая, модная и помпезная комната.'
        }


class MeetingRoomUpdate(MeetingRoomBase):
    name: None | str = Field(
        None,
        title="Название комнаты",
        min_length=1,
        max_length=100
    )


class MeetingRoomResponse(MeetingRoomBase):
    """Схема ответа после создания новых MeetingRoom.
    """
    id: int

    class Config:
        title = "Схема ответа после создания новых MeetingRoom"
        orm_mode = True
        schema = {
                'id': 5,
                'name': 'Главная переговорка',
                'description': 'Очень большая, модная и помпезная комната.'
        }
