from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.dependencies.base_dependencies import SessionDep
from app.core.exceptions import ForbiddenError, UnauthorizedError, UserNotFoundError
from app.core.roles import UserRole
from app.core.security import decode_token
from app.models.users import UserModel
import app.repositories.user_repository as user_repository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


async def get_current_user(
    session: SessionDep,
    token: str = Depends(oauth2_scheme),
):
    payload = decode_token(token)
    user_id = payload.get("sub")
    if user_id is None:
        raise UnauthorizedError("Invalid token")

    user = await user_repository.get_user_by_id(
        session,
        int(user_id),
    )
    if user is None:
        raise UserNotFoundError()

    return user


async def get_current_admin(
    current_user: UserModel = Depends(get_current_user),
):
    if current_user.role != UserRole.ADMIN:
        raise ForbiddenError()

    return current_user
