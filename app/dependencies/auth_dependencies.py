from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from app.dependencies.base_dependencies import SessionDep
from app.core.security import decode_token
import app.repositories.user_repository as user_repository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


async def get_current_user(
    session: SessionDep,
    token: str = Depends(oauth2_scheme),
):
    payload = decode_token(token)
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
        )
    user = await user_repository.get_user_by_id(
        session,
        int(user_id),
    )
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found",
        )
    return user
