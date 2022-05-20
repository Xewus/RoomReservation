from fastapi import APIRouter

from app.api import endpoints as ends

main_router = APIRouter()

main_router.include_router(
    ends.meeting_room_router, prefix='/meeting_rooms',
    tags=['Meeting Rooms']
)
main_router.include_router(
    ends.reservation_router, prefix='/reservations',
    tags=['Reservations']
)
main_router.include_router(
    ends.user_router
)
