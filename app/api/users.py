from fastapi import APIRouter
from sqlalchemy import select
from app.dependencies.base_dependencies import SessionDep
from app.models.users import UserModel
from app.schemas.users import UserSchema

router = APIRouter()


@router.post("/users")
async def add_user(data: UserSchema, session: SessionDep):
    new_user = UserModel(login=data.login, password=data.password, role=data.role)
    session.add(new_user)
    await session.commit()
    return {"message": "User added successfully."}


@router.get("/users")
async def get_users(session: SessionDep):
    query = select(UserModel)
    result = await session.execute(query)
    return result.scalars().all()
