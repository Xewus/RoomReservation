from typing import Generic, Type, TypeVar
from fastapi.encoders import jsonable_encoder

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base
from app.schemas import user as user_schema

ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Базовый класс для операций CRUD.
    """
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def create(
        self,
        data: CreateSchemaType,
        session: AsyncSession,
        user: None | user_schema.UserDB = None
    ) -> ModelType:
        """Создаёт запись в БД.

        ### Args:
        - data (CreateSchemaType): Данные для записи в БД.
        - session (AsyncSession): Объект сессии.
        - user (None | user_schema.UserDB, optional):
            Пользователь, связанный с записью.
            Defaults to None.

        ### Returns:
        - ModelType: Объект, записаный в БД.
        """
        data = data.dict()
        if user is not None:
            data['user_id'] = user.id
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
        - obj (Base): Редактируемый объект.
        - update_data (UpdateSchemaType): Обновляемые данные.
        - session (AsyncSession): Объект сессии.

        ### Returns:
        - ModelType: Обновлённый объект.
        """
        obj_data = jsonable_encoder(obj)
        update_data = update_data.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(obj, field, update_data[field])

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
        - obj (Base): Удаляемый объект.
        - session (AsyncSession): Объект сессии.

        ### Returns:
        - ModelType:
            Удалённый объект.
            Данные объекта всё ещё хранятся в сессии после удаления из БД.
        """
        await session.delete(obj)
        await session.commit()
        return obj

    async def get(
        self,
        obj_id: int,
        session: AsyncSession
    ) -> None | ModelType:
        """Получает объект из БД по id.

        ### Args:
        - obj_id (int): id искомого объекта.
        - session (AsyncSession): Объект сессии.

        ### Returns:
        - None | ModelType: Найденный объект.
        """
        return await session.get(self. model, obj_id)

    async def get_all(
        self,
        session: AsyncSession
    ) -> list[ModelType]:
        """Возвращает все объекты из таблицы.

        ### Args:
        - session (AsyncSession): Объект сессии.

        ### Returns:
        - list[ModelType]: Список объектов.
        """
        objects = await session.scalars(
            select(self.model)
        )
        return objects.all()

    async def get_by_field(
        self,
        field: str,
        value,
        session: AsyncSession
    ) -> None | ModelType:
        """Находит один объект по значению указанного поля.

        ### Args:
        - field (str): Поле, по которому ведётся поиск.
        - value (_type_): Искомое значение.
        - session (AsyncSession): Объект сессии.

        ### Raises:
        - AttributeError: Указанное поле отсутствует в таблице.

        ### Returns:
        - None | ModelType:Найденный объект.
        """
        field = getattr(self.model, field)
        if field is None:
            raise AttributeError
        return await session.scalar(
            select(self.model).where(field == value)
        )

    async def value_in_db_exist(
        self,
        field: str,
        value,
        session: AsyncSession,
        id: None | int = None,
    ) -> bool:
        """Проверяет наличие значения в запрошенном поле таблицы.

        ### Args:
        - field (str): Поле, по которому ведётся поиск.
        - value (_type_): Искомое значение.
        - session (AsyncSession): Объект сессии.
        - id (None | int, optional):
            id объекта, в полях которого необходимо вести поиск.
            Defaults to None.

        ### Raises:
        - AttributeError: Указанное поле отсутствует в таблице.

        ### Returns:
        - bool: Найдено или нет переданное значение.
        """
        if id is None:
            return bool(await self.get_by_field(field, value, session))

        field = getattr(self.model, field)
        if field is None:
            raise AttributeError

        return bool(await session.scalar(select(self.model.id).where(
            field == value, self.model.id != id
        ).limit(1)))
