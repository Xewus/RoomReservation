from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable

from app.core import db


class UserTable(SQLAlchemyBaseUserTable, db.Base):
    """Таблица в БД для пользователей и их администрирования.
    """
    pass
