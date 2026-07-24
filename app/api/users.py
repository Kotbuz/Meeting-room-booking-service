from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from app.core import security
from app.dependencies.base_dependencies import SessionDep
from app.models.users import UserModel
from app.services.user_service import (
    get_user_by_login_service,
    get_user_by_id_service,
    get_users_by_role_service,
    get_all_users_service,
    create_user_service,
    update_user_service,
    partial_update_user_service,
)
from app.schemas.users import UserCreateSchema, UserResponseSchema, UserUpdateSchema

router = APIRouter(tags=["Users"])


@router.post("/", status_code=201, response_model=UserResponseSchema)
async def add_user(data: UserCreateSchema, session: SessionDep):
    return await create_user_service(session, data.login, data.password, data.role)


@router.get("/", response_model=list[UserResponseSchema])
async def get_users(session: SessionDep):
    return await get_all_users_service(session)


@router.get("/{id}", response_model=UserResponseSchema)
async def get_user_by_id(id: int, session: SessionDep):
    user = await get_user_by_id_service(session, id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )
    return user


@router.get("/role/{role}", response_model=list[UserResponseSchema])
async def get_users_by_role(role: str, session: SessionDep):
    return await get_users_by_role_service(session, role)


@router.delete("/{id}", status_code=204)
async def delete_user(id: int, session: SessionDep):
    user = await get_user_by_id_service(session, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await session.delete(user)
    await session.commit()
    return


@router.put("/{id}", response_model=UserResponseSchema)
async def update_user(id: int, data: UserCreateSchema, session: SessionDep):
    return await update_user_service(session, id, data)


@router.patch("/{id}", response_model=UserResponseSchema)
async def partial_update_user(id: int, data: UserUpdateSchema, session: SessionDep):
    return await partial_update_user_service(session, id, data)
