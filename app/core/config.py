from typing import Union

import pydantic as pd


class Settings(pd.BaseSettings):
    """Настройки проекта.
    """
    debug: bool =          False
    echo: bool =           False
    app_title: str =       'Booking meeting rooms'
    version: str =         '2.0.0'
    description: str =     'Really cool project'
    database_url: str =    'sqlite+aiosqlite:///./test.db'
    secret: str =          'SECRET'
    # for auto_create first superuser
    first_superuser_email: Union[None, pd.EmailStr] = None
    first_superuser_password: Union[None, str] =      None
    # for Google API
    type_: Union[None, str] =                         None
    project_id: Union[None, str] =                    None
    private_key_id: Union[None, str] =                None
    private_key: Union[None, str] =                   None
    client_email: Union[None, str] =                  None
    client_id: Union[None, str] =                     None
    auth_uri: Union[None, str] =                      None
    token_uri: Union[None, str] =                     None
    auth_provider_x509_cert_url: Union[None, str] =   None
    client_x509_cert_url: Union[None, str] =          None
    email_user: Union[None, str] =                    None

    class Config:
        env_file = '.env'


settings = Settings()

if settings.debug:
    settings.echo = True
