from datetime import datetime

from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import db, user
from app.core import google_client as google
from app.services import google_api as google_serv
from app.services import constants as const

from app.crud.reservation import reservation_crud as rsr_crud

from pprint import pprint

router = APIRouter()


@router.post(
    path='/',
    summary=const.API_GOOGLE_UPLOAD,
    response_model=list[dict[str, int]],
    dependencies=[Depends(user.current_superuser)]
)
async def det_report(
    start_time: datetime,
    end_time: datetime,
    session: AsyncSession = Depends(db.get_async_session),
    wrapper_service: Aiogoogle = Depends(google.get_service)
) -> list[dict[str, int]]:
    """Только для суперюзеров."""
    count_reservations = await rsr_crud.count_reses_in_time_interval(
        start_time=start_time,
        end_time=end_time,
        session=session
    )
    spreadsheet_id = await google_serv.spreadsheet_create(wrapper_service)
    await google_serv.set_user_permissions(spreadsheet_id, wrapper_service)
    await google_serv.spreadsheet_update_value(
        spreadsheet_id, count_reservations, wrapper_service
    )
    return count_reservations
