from sqlalchemy.ext.asyncio import AsyncSession

from fastapi.security import OAuth2PasswordRequestForm
from app.core.exceptions import InvalidCredentialsError, UserNotFoundError
import app.repositories.user_repository as user_repo
import app.core.security as security


async def login(
    session: AsyncSession,
    form_data: OAuth2PasswordRequestForm,
):
    user = await user_repo.get_user_by_login(session, form_data.username)
    if not user:
        raise UserNotFoundError()
    if not security.verify_password(form_data.password, user.password_hash):
        raise InvalidCredentialsError()
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
