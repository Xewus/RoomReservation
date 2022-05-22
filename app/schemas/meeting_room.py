from pydantic import BaseModel, Field, validator

from app.core import literals as lit


class MeetingRoomBase(BaseModel):
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

    class Config:
        orm_mode = True
        title = "Схема для обновления MeetingRoom"

    @validator('name')
    def not_null_name(cls, name: str):
        if name is None:
            raise ValueError(lit.ERR_NULL_VALUE % 'name')
        return name


class MeetingRoomResponse(MeetingRoomBase):
    id: int

    class Config:
        title = "Схема ответа после создания новых MeetingRoom"
        orm_mode = True
        schema = {
                'id': 5,
                'name': 'Главная переговорка',
                'description': 'Очень большая, модная и помпезная комната.'
        }
