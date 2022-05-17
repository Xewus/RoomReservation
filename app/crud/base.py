from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel as input_data

from app.core.db import Base


class CRUDBase:
    """Базовый класс для операций CRUD.
    """
    def __init__(self, model):
        self.model = model

    async def get(
        self,
        obj_id: int,
        session: AsyncSession
    ) -> Base:
        """Получает объект из БД по id.

        ### Args:
        - obj_id (int): _description_
        - session (AsyncSession): _description_

        ### Returns:
        - _type_: _description_
        """
        return await session.get(
            select(self.model).where(self.model.id == obj_id)
        )

    async def get_all(
        self,
        session: AsyncSession
    ) -> list[Base]:
        """Возвращает все объекты из таблицы.

        ### Args:
        - session (AsyncSession): _description_

        ### Returns:
        - _type_: _description_
        """
        objects = await session.scalars(
            select(self.model)
        )
        return objects.all()

    async def create(
        self,
        data: input_data,
        session: AsyncSession
    ) -> Base:
        """Создаёт запись в БД.

        ### Args:
        - obj_in (BaseModel): _description_
        - session (AsyncSession): _description_

        ### Returns:
        - Base: _description_
        """
        data = data.dict()
        obj = self.model(**data)
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj

    async def update(
        self,
        obj: Base,
        update_data: input_data,
        session: AsyncSession
    ):
        """Обновляет запись в БД.

        ### Args:
        - obj (Base): _description_
        - update_data (input_data): _description_
        - session (AsyncSession): _description_

        ### Returns:
        - _type_: _description_
        """
        for field, value in update_data.dict(exclude_unset=True).items():
            if getattr(obj, field):
                setattr(obj, field, value)
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj

    async def remove(
        self,
        obj: Base,
        session: AsyncSession
    ):
        """Удаляет запись из БД.

        ### Args:
        - obj (Base): _description_
        - session (AsyncSession): _description_

        ### Returns:
        - _type_: _description_
        """
        await session.delete(obj)
        await session.commit()
        return obj

    async def get_by_attribute(
            self, 
            attr_name: str, 
            attr_value: str,
            session: AsyncSession,
    ):
        attr = getattr(self.model, attr_name)
        db_obj = await session.execute(
            select(self.model).where(attr == attr_value)
        )
        return db_obj.scalars().first()

    async def value_in_db_exist(
        self,
        field: str,
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
        field = getattr(self, field)
        if id is not None:
            table_id = getattr(self, 'id')
            query = select(field).where(
                field == value, table_id != id
            ).limit(1)
        else:
            query = select(field).where(field == value).limit(1)
        return bool(await session.scalar(query))
