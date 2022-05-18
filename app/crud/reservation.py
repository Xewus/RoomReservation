from .base import CRUDBase
from app.models.reservation import Reservation
from app.schemas.reservation import ReservationCreate, ReservationUpdate


reservation_crud = CRUDBase[
    Reservation,
    ReservationCreate,
    ReservationUpdate
](Reservation)
