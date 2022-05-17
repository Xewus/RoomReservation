from .base import CRUDBase
from app.models.reservation import Reservation


crud = CRUDBase(Reservation)
