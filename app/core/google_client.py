"""Настройки для подключения к GoogleAPI.
"""
from aiogoogle import Aiogoogle
from aiogoogle.auth.creds import ServiceAccountCreds

from app.core.config import settings

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

INFO = {
    'type': settings.type_,
    'project_id': settings.project_id,
    'private_key_id': settings.private_key_id,
    'private_key': settings.private_key,
    'client_email': settings.client_email,
    'client_id': settings.client_id,
    'auth_uri': settings.auth_uri,
    'token_uri': settings.token_uri,
    'auth_provider_x509_cert_url': settings.auth_provider_x509_cert_url,
    'client_x509_cert_url': settings.client_x509_cert_url
}
# Получаем объект учётных данных
credentials = ServiceAccountCreds(scopes=SCOPES, **INFO)


async def get_service():
    """Создаёт экземпляр класса Aiogoogle.

    ### Yields:
    - Aiogoogle
    """
    async with Aiogoogle(service_account_creds=credentials) as aiogoogle:
        yield aiogoogle
