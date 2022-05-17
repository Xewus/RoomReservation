from pydantic import BaseModel, Field, validator

from app.core import literals as lit


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
    """Схема для создания новых MeetingRoom.
    """

    class Config:
        orm_mode = True
        title = "Схема для создания новых MeetingRoom"
        schema = {
                'name': 'Главная переговорка',
                'description': 'Очень большая, модная и помпезная комната.'
        }


class MeetingRoomUpdate(MeetingRoomBase):
    """Схема для обновления MeetingRoom.
    """
    name: None | str = Field(
        None,
        title="Название комнаты",
        min_length=1,
        max_length=100
    )

    class Config:
        orm_mode = True
        title = "Схема для обновления MeetingRoom"

    @validator('name')
    def not_null_name(cls, value):
        if value is None:
            raise ValueError(lit.ERR_NULL_VALUE % 'name')
        return value


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
