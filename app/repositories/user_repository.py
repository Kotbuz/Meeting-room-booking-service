from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.users import UserModel


async def save(session: AsyncSession):
    try:
        await session.commit()
    except:
        await session.rollback()
        raise


async def refresh(session: AsyncSession, instance):
    await session.refresh(instance)
    return instance


async def get_user_by_login(session: AsyncSession, login: str):
    query = select(UserModel).where(UserModel.login == login)
    result = await session.execute(query)
    return result.scalar_one_or_none()


async def get_user_by_id(session: AsyncSession, user_id: int):
    return await session.get(UserModel, user_id)


async def get_users_by_role(session: AsyncSession, role: str):
    query = select(UserModel).where(UserModel.role == role)
    result = await session.execute(query)
    return result.scalars().all()


async def get_all_users(session: AsyncSession):
    query = select(UserModel)
    result = await session.execute(query)
    return result.scalars().all()


async def create_user(
    session: AsyncSession, login: str, hashed_password: str, role: str
):
    new_user = UserModel(login=login, password_hash=hashed_password, role=role)
    session.add(new_user)
    return new_user


async def update_user(
    user: UserModel,
    login: str,
    hashed_password: str,
    role: str,
):
    user.login = login
    user.password_hash = hashed_password
    user.role = role
    return user


async def partial_update_user(
    user: UserModel,
    login: str = None,
    hashed_password: str = None,
    role: str = None,
):
    if login is not None:
        user.login = login
    if hashed_password is not None:
        user.password_hash = hashed_password
    if role is not None:
        user.role = role
    return user


async def delete_user(session: AsyncSession, user: UserModel):
    await session.delete(user)
