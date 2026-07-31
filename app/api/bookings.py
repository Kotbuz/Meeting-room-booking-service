from fastapi import APIRouter, Depends, HTTPException

from app.core.roles import UserRole
from app.dependencies.auth_dependencies import get_current_admin, get_current_user
from app.dependencies.base_dependencies import SessionDep
from app.models.users import UserModel
from app.schemas.bookings import (
    BookingCreateSchema,
    BookingResponseSchema,
    BookingUpdateSchema,
)
import app.services.booking_service as service

router = APIRouter(tags=["Bookings"])


@router.post("/", status_code=201, response_model=BookingResponseSchema)
async def create_booking(
    session: SessionDep,
    data: BookingCreateSchema,
    current_user: UserModel = Depends(get_current_user),
):
    data.user_id = current_user.id
    return await service.create_booking(session, data)


@router.get("/", response_model=list[BookingResponseSchema])
async def get_bookings(
    session: SessionDep,
    current_user: UserModel = Depends(get_current_user),
):
    if current_user.role == UserRole.ADMIN:
        return await service.get_all_bookings(session)
    return await service.get_bookings_by_user(session, current_user.id)


@router.get("/{id}", response_model=BookingResponseSchema)
async def get_booking_by_id(
    session: SessionDep,
    id: int,
    current_user: UserModel = Depends(get_current_user),
):
    booking = await service.get_booking_by_id(session, id)
    if not booking:
        raise HTTPException(404, "Booking not found")
    if current_user.role != UserRole.ADMIN and booking.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Access denied",
        )
    return booking


@router.get("/user/{user_id}", response_model=list[BookingResponseSchema])
async def get_bookings_by_user(
    session: SessionDep,
    user_id: int,
    current_user: UserModel = Depends(get_current_user),
):
    if current_user.role != UserRole.ADMIN and current_user.id != user_id:
        raise HTTPException(
            status_code=403,
            detail="Access denied",
        )
    return await service.get_bookings_by_user(session, user_id)


@router.put("/{id}", response_model=BookingResponseSchema)
async def update_booking(
    session: SessionDep,
    id: int,
    data: BookingCreateSchema,
    current_user: UserModel = Depends(get_current_user),
):
    booking = await service.get_booking_by_id(session, id)
    if not booking:
        raise HTTPException(404, "Booking not found")
    if current_user.role != UserRole.ADMIN and booking.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Access denied",
        )
    data.user_id = (
        current_user.id if current_user.role != UserRole.ADMIN else data.user_id
    )
    return await service.update_booking(session, id, data)


@router.patch("/{id}", response_model=BookingResponseSchema)
async def partial_update_booking(
    session: SessionDep,
    id: int,
    data: BookingUpdateSchema,
    current_user: UserModel = Depends(get_current_user),
):
    booking = await service.get_booking_by_id(session, id)
    if not booking:
        raise HTTPException(404, "Booking not found")
    if current_user.role != UserRole.ADMIN and booking.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Access denied",
        )
    if current_user.role != UserRole.ADMIN:
        data.user_id = current_user.id
    return await service.partial_update_booking(session, id, data)


@router.delete("/{id}", status_code=204)
async def delete_booking(
    session: SessionDep,
    id: int,
    current_user: UserModel = Depends(get_current_user),
):
    booking = await service.get_booking_by_id(session, id)
    if not booking:
        raise HTTPException(404, "Booking not found")

    if current_user.role != UserRole.ADMIN and booking.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Access denied",
        )

    await service.delete_booking(session, id)
