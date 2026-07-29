from fastapi import APIRouter
from fastapi import Depends

from app.dependencies.auth_dependencies import get_current_user
from app.models.users import UserModel
from app.schemas.users import UserResponseSchema

from app.dependencies.base_dependencies import SessionDep
from app.schemas.auth import LoginSchema, TokenSchema
import app.services.auth_service as service

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=TokenSchema)
async def login(
    session: SessionDep,
    data: LoginSchema,
):
    return await service.login(session, data)


@router.get(
    "/me",
    response_model=UserResponseSchema,
)
async def get_me(
    current_user: UserModel = Depends(get_current_user),
):
    return current_user
