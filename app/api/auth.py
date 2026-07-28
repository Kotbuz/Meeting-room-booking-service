from fastapi import APIRouter

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
