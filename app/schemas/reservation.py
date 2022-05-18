from datetime import datetime

from pydantic import BaseModel, Field, root_validator, validator

from app.core import literals as lit


class ReservationBase(BaseModel):
    start_time: datetime = Field(
        ...,
        title='Начало брони'
    )
    end_time: datetime = Field(
        ...,
        title='Конец брони'
    )

    class Config:
        orm_mode = True

    @root_validator(skip_on_failure=True)
    def reserv_validate(cls, values: dict):
        start = values.get('start_time')
        end = values.get('end_time')
        if not (start and end):
            raise ValueError(
                lit.ERR_NOT_ENOUGH_VALUES % 'start_time, end_time'
            )
        if end < start:
            raise ValueError(
                lit.ERR_TIME_RESERVATION % start, end
            )
        return values


class ReservationUpdate(ReservationBase):

    @validator('start_time')
    def check_start_time(cls, value: datetime):
        if datetime.now() > value:
            raise ValueError(lit.ERR_START_TIME)
        return value


class ReservationCreate(ReservationUpdate):
    room_id: int = Field(
        ...,
        title='Номер комнаты'
    )


class ReservationResponse(ReservationBase):
    id: int = Field(
        ...,
        title='id брони'
    )
    room_id: int = Field(
        ...,
        title='Номер комнаты'
    )
