from typing import Generic, Type, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.core.db import Base


ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Базовый класс для операций CRUD.
    """
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get_by_field(
        self,
        field: str,
        value,
        session: AsyncSession
    ) -> None | ModelType:
        """Находит один объект по значению указанного поляю

        ### Args:
        - field (str): _description_
        - value (_type_): _description_
        - session (AsyncSession): _description_

        ### Raises:
        - AttributeError: _description_

        ### Returns:
        - Base: _description_
        """
        field = getattr(self.model, field)
        if field is None:
            raise AttributeError
        return await session.scalar(
            select(self.model).where(field == value)
        )

    async def get(
        self,
        obj_id: int,
        session: AsyncSession
    ) -> None | ModelType:
        """Получает объект из БД по id.

        ### Args:
        - obj_id (int): _description_
        - session (AsyncSession): _description_

        ### Returns:
        - _type_: _description_
        """
        return await self.get_by_field('id', obj_id, session)

    async def get_all(
        self,
        session: AsyncSession
    ) -> list[ModelType]:
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
        data: CreateSchemaType,
        session: AsyncSession
    ) -> ModelType:
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
        update_data: UpdateSchemaType,
        session: AsyncSession
    ) -> ModelType:
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
    ) -> ModelType:
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
        if id is None:
            return bool(await self.get_by_field(field, value, session))

        field = getattr(self.model, field)
        if field is None:
            raise AttributeError
        return bool(await session.scalar(select(self.model.id).where(
            field == value, self.model.id != id
        ).limit(1)))
