from fastapi import APIRouter

from app.api.users import router as users_router
from app.api.bookings import router as bookings_router
from app.api.rooms import router as rooms_router
from app.api.timeslots import router as timeslots_router


main_router = APIRouter()

main_router.include_router(users_router, prefix="/api/users")
main_router.include_router(bookings_router, prefix="/api/bookings")
main_router.include_router(rooms_router, prefix="/api/rooms")
main_router.include_router(timeslots_router, prefix="/api/timeslots")
