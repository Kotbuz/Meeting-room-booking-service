from fastapi import APIRouter, Depends, HTTPException
from app.core.roles import UserRole
from app.dependencies.auth_dependencies import get_current_admin
from app.dependencies.base_dependencies import SessionDep
import app.services.user_service as service
from app.schemas.users import UserCreateSchema, UserResponseSchema, UserUpdateSchema

router = APIRouter(tags=["Users"])


@router.post(
    "/",
    status_code=201,
    response_model=UserResponseSchema,
)
async def create_user(
    session: SessionDep,
    data: UserCreateSchema,
    current_user=Depends(get_current_admin),
):
    return await service.create_user(session, data)


@router.get("/", response_model=list[UserResponseSchema])
async def get_users(
    session: SessionDep,
    current_user=Depends(get_current_admin),
):
    return await service.get_all_users(session)


@router.get("/{id}", response_model=UserResponseSchema)
async def get_user_by_id(
    session: SessionDep,
    id: int,
    current_user=Depends(get_current_admin),
):
    user = await service.get_user_by_id(session, id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )
    return user


@router.get("/role/{role}", response_model=list[UserResponseSchema])
async def get_users_by_role(
    session: SessionDep,
    role: UserRole,
    current_user=Depends(get_current_admin),
):
    return await service.get_users_by_role(session, role)


@router.delete("/{id}", status_code=204)
async def delete_user(
    session: SessionDep,
    id: int,
    current_user=Depends(get_current_admin),
):
    await service.delete_user(session, id)


@router.put("/{id}", response_model=UserResponseSchema)
async def update_user(
    session: SessionDep,
    id: int,
    data: UserCreateSchema,
    current_user=Depends(get_current_admin),
):
    return await service.update_user(session, id, data)


@router.patch("/{id}", response_model=UserResponseSchema)
async def partial_update_user(
    session: SessionDep,
    id: int,
    data: UserUpdateSchema,
    current_user=Depends(get_current_admin),
):
    return await service.partial_update_user(session, id, data)
