from fastapi import FastAPI

from app.core.config import settings

app = FastAPI(
    title=settings.app_title,
    description=settings.description,
    debug=settings.debug,
    version=settings.version,
)
