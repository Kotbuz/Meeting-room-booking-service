import hashlib

from fastapi import APIRouter
from sqlalchemy import select
from app.dependencies.base_dependencies import SessionDep
from app.models.users import UserModel
from app.schemas.users import UserAddSchema

router = APIRouter(tags=["Users"])


@router.post("/users")
async def add_user(data: UserAddSchema, session: SessionDep):
    hashed_password = hashlib.sha256(data.password.encode()).hexdigest()
    new_user = UserModel(
        login=data.login, password_hash=hashed_password, role=data.role
    )
    session.add(new_user)
    await session.commit()
    return {"message": "User added successfully."}


@router.get("/users")
async def get_users(session: SessionDep):
    query = select(UserModel)
    result = await session.execute(query)
    return result.scalars().all()
