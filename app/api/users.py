from fastapi import APIRouter, HTTPException
from app.dependencies.base_dependencies import SessionDep
import app.services.user_service as service
from app.schemas.users import UserCreateSchema, UserResponseSchema, UserUpdateSchema

router = APIRouter(tags=["Users"])


@router.post("/", status_code=201, response_model=UserResponseSchema)
async def create_user(session: SessionDep, data: UserCreateSchema):
    return await service.create_user(session, data)


@router.get("/", response_model=list[UserResponseSchema])
async def get_users(session: SessionDep):
    return await service.get_all_users(session)


@router.get("/{id}", response_model=UserResponseSchema)
async def get_user_by_id(session: SessionDep, id: int):
    user = await service.get_user_by_id(session, id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )
    return user


@router.get("/role/{role}", response_model=list[UserResponseSchema])
async def get_users_by_role(session: SessionDep, role: str):
    return await service.get_users_by_role(session, role)


@router.delete("/{id}", status_code=204)
async def delete_user(session: SessionDep, id: int):
    await service.delete_user(session, id)


@router.put("/{id}", response_model=UserResponseSchema)
async def update_user(
    session: SessionDep,
    id: int,
    data: UserCreateSchema,
):
    return await service.update_user(session, id, data)


@router.patch("/{id}", response_model=UserResponseSchema)
async def partial_update_user(session: SessionDep, id: int, data: UserUpdateSchema):
    return await service.partial_update_user(session, id, data)
