import pydantic as pd


class Settings(pd.BaseSettings):
    """Настройки проекта.
    """
    debug: bool = False
    echo: bool = False
    app_title: str = 'Booking meeting rooms'
    version: str = '0.0.0'
    description: str = 'Really cool project'
    database_url: str

    class Config:
        env_file = '.env'


settings = Settings()

if settings.debug:
    settings.echo = True
