from datetime import datetime
from pydantic import BaseModel, Field, validator, root_validator

from app.core import literals as lit


class ReservationBase(BaseModel):
    from_reserve: datetime = Field(
        ...,
        title='Начало брони'
    )
    to_reserve: datetime = Field(
        ...,
        title='Конец брони'
    )

    class Config:
        orm_mode = True

    @root_validator(skip_on_failure=True)
    def reserv_validate(cls, values: dict):
        start = values.get('from_reserve')
        end = values.get('to_reserve')
        if not (start and end):
            raise ValueError(
                lit.ERR_NOT_ENOUGH_VALUES % ('from_reserve', 'to_reserve')
            )
        if end < start:
            raise ValueError(
                lit.ERR_TIME_RESERVATION % start, end
            )
        return values


class ReservationUpdate(ReservationBase):

    @validator('from_reserve')
    def check_from_reserve(cls, value: datetime):
        if datetime.now() < value:
            raise ValueError(lit.ERR_START_TIME)
        return value


class ReservationCreate(ReservationUpdate):
    meetingroom_id: int = Field(
        ...,
        title='Номер комнаты'
    )


class ReservationRespons(ReservationBase):
    id: int = Field(
        ...,
        title='id брони'
    )
    meetingroom_id: int = Field(
        ...,
        title='Номер комнаты'
    )
