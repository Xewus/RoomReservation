import pydantic as pd


class Settings(pd.BaseSettings):
    debug: str = False
    app_title: str = 'Room appointments'
    version: str = '0.0.0'
    description: str = 'Really cool project'

    class Config:
        env_file = '.env'


settings = Settings()
