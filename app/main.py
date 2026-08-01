from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import main_router
from app.core.config import settings
from app.core.exceptions import AppException
from app.core.roles import UserRole
from app.core.security import hash_password
from app.db.database import new_session
from app.models.users import UserModel
import app.repositories.user_repository as user_repository


async def create_default_admin_user(session: AsyncSession | None = None) -> None:
    if session is None:
        async with new_session() as session:
            await create_default_admin_user(session)
        return

    existing_user = await user_repository.get_user_by_login(
        session,
        settings.admin_login,
    )
    if existing_user is not None:
        return

    admin_user = UserModel(
        login=settings.admin_login,
        password_hash=hash_password(settings.admin_password),
        role=UserRole.ADMIN,
    )
    session.add(admin_user)
    await user_repository.save(session)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_default_admin_user()
    yield


app = FastAPI(lifespan=lifespan)


@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


app.include_router(main_router)
