from fastapi import FastAPI

from app.api import meeting_room as mr_api
from app.core.config import settings

app = FastAPI(
    title=settings.app_title,
    description=settings.description,
    debug=settings.debug,
    version=settings.version,
)

app.include_router(mr_api.router)
