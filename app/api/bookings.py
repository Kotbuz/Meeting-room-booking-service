from fastapi import APIRouter, HTTPException

from app.dependencies.base_dependencies import SessionDep
from app.schemas.bookings import (
    BookingCreateSchema,
    BookingResponseSchema,
    BookingUpdateSchema,
)
import app.services.booking_service as service

router = APIRouter(tags=["Bookings"])


@router.post("/", status_code=201, response_model=BookingResponseSchema)
async def create_booking(session: SessionDep, data: BookingCreateSchema):
    return await service.create_booking(session, data)


@router.get("/", response_model=list[BookingResponseSchema])
async def get_bookings(session: SessionDep):
    return await service.get_all_bookings(session)


@router.get("/{id}", response_model=BookingResponseSchema)
async def get_booking_by_id(session: SessionDep, id: int):
    booking = await service.get_booking_by_id(session, id)
    if not booking:
        raise HTTPException(404, "Booking not found")
    return booking


@router.get("/user/{user_id}", response_model=list[BookingResponseSchema])
async def get_bookings_by_user(session: SessionDep, user_id: int):
    return await service.get_bookings_by_user(session, user_id)


@router.put("/{id}", response_model=BookingResponseSchema)
async def update_booking(
    session: SessionDep,
    id: int,
    data: BookingCreateSchema,
):
    return await service.update_booking(session, id, data)


@router.patch("/{id}", response_model=BookingResponseSchema)
async def partial_update_booking(
    session: SessionDep,
    id: int,
    data: BookingUpdateSchema,
):
    return await service.partial_update_booking(session, id, data)


@router.delete("/{id}", status_code=204)
async def delete_booking(session: SessionDep, id: int):
    await service.delete_booking(session, id)
