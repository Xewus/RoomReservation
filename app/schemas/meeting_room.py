from pydantic import BaseModel, validator


class MeetingRoomCreate(BaseModel):
    """Схема приёма значений для создания  MeetingRoom.

    ## Attrs:
    - name: Название комнаты.
    - description: Описание комнаты.
    """
    name: str
    description: str = None

    class Config:
        title = "Создание новых MeetingRoom"
        schema = {
            'example': {
                'name': 'Главная переговорка',
                'description': 'Очень большая, модная и помпезная комната.'
            }
        }

    @validator('name')
    def len_string(cls, value: str) -> str:
        """Проверяет допустимую длину значения.

        ## Args:
        - value (str): Проверяемое значение.

        ## Raises:
        - ValueError: Значение больше ограничения.

        ## Returns:
        - str: Проверенное значение.
        """
        if len(value) > 100:
            raise ValueError(f'{value.__name__} is too long. Max: 100 symbols')
        return value
