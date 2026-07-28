from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.auth import LoginSchema
import app.repositories.user_repository as user_repo
import app.core.security as security


async def login(
    session: AsyncSession,
    data: LoginSchema,
):
    user = await user_repo.get_user_by_login(session, data.login)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not security.verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect password")
    token = security.create_access_token(
        {
            "sub": str(user.id),
            "role": user.role,
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer",
    }


def create_access_token(data: dict): ...
