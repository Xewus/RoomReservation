"""Функции взаимодействия приложения с Google API.
"""
from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings
from app.services import constants as const


async def spreadsheet_create(wrapper_services: Aiogoogle) -> str:
    """Создаёт таблицу.

    ### Args:
    - wrapper_service (Aiogoogle):
        ...

    ### Returns:
    - str:
        `id` созданной таблицы.
    """
    now_date_time = datetime.now().strftime(const.DATE_FORMAT)
    service = await wrapper_services.discover(
        api_name='sheets',
        api_version='v4'
    )
    spreadsheet_body = {
        'properties': {
            'title': f'Отчет на {now_date_time}',
            'locale': 'ru_RU'
        },
        'sheets': [
            {'properties': {
                'sheetType': 'GRID',
                'sheetId': 0,
                'title': 'Лист1',
                'gridProperties': {
                    'rowCount': 100,
                    'columnCount': 11
                }
            }}
        ]
    }
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    return response['spreadsheetId']


async def set_user_permissions(
    spreadsheet_id: str,
    wrapper_service: Aiogoogle
) -> None:
    """Получает разрешение на доступ к таблице.

    ### Args:
    - spreadsheet_id (str):
        `id` таблицы.
    - wrapper_service (Aiogoogle):
        ...
    """
    permissions_body = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': settings.email_user
    }
    service = await wrapper_service.discover(
        api_name='drive',
        api_version='v3'
    )
    await wrapper_service.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=permissions_body,
            fields='id'
        )
    )


async def spreadsheet_update_value(
    spreadsheet_id: str,
    reservations: list,
    wrapper_service: Aiogoogle
) -> None:
    now_date_time = datetime.now().strftime(const.DATE_FORMAT)
    service = await wrapper_service.discover(
        api_name='sheets',
        api_version='v4'
    )
    # Тело таблицы
    table_values = [
        ['Отчет от', now_date_time],
        ['Количество регистраций переговорок'],
        ['ID переговорки', 'Кол-во бронирований']
    ]
    for res in reservations:
        table_values.append([str(res['room_id'])])
    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    response = await wrapper_service.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range='A1:E30',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
