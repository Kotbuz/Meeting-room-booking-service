# from fastapi import HTTPException
# from sqlalchemy.ext.asyncio import AsyncSession

# from app.core import security

# import app.repositories.user_repository as repository
# from app.schemas.users import UserCreateSchema, UserUpdateSchema


# async def create_user(session: AsyncSession, data: UserCreateSchema):
#     hashed_password = security.hash_password(data.password)
#     existing_user = await repository.get_user_by_login(session, data.login)
#     if existing_user:
#         raise HTTPException(
#             status_code=400, detail="User with this login already exists"
#         )
#     new_user = await repository.create_user(
#         session, data.login, hashed_password, data.role
#     )
#     await repository.save(session)
#     await repository.refresh(session, new_user)
#     return new_user


# async def get_user_by_login(session: AsyncSession, login: str):
#     return await repository.get_user_by_login(session, login)


# async def get_user_by_id(session: AsyncSession, user_id: int):
#     return await repository.get_user_by_id(session, user_id)


# async def get_users_by_role(session: AsyncSession, role: str):
#     return await repository.get_users_by_role(session, role)


# async def get_all_users(session: AsyncSession):
#     return await repository.get_all_users(session)


# async def update_user(session: AsyncSession, user_id: int, data: UserUpdateSchema):
#     user = await repository.get_user_by_id(session, user_id)
#     if not user:
#         raise HTTPException(status_code=404, detail="User does not exists")

#     existing_user = await repository.get_user_by_login(session, data.login)

#     if existing_user and existing_user.id != user.id:
#         raise ValueError("User with this login already exists")

#     hashed_password = security.hash_password(data.password)
#     updated_user = await repository.update_user(
#         user, data.login, hashed_password, data.role
#     )
#     await repository.save(session)
#     await repository.refresh(session, updated_user)
#     return updated_user


# async def partial_update_user(
#     session: AsyncSession, user_id: int, data: UserUpdateSchema
# ):
#     user = await repository.get_user_by_id(session, user_id)
#     if not user:
#         raise HTTPException(status_code=404, detail="User does not exists")
#     if data.login is not None:
#         existing_user = await repository.get_user_by_login(session, data.login)

#         if existing_user and existing_user.id != user.id:
#             raise ValueError("User with this login already exists")

#     hashed_password = security.hash_password(data.password) if data.password else None
#     updated_user = await repository.partial_update_user(
#         user,
#         login=data.login,
#         hashed_password=hashed_password,
#         role=data.role,
#     )
#     await repository.save(session)
#     await repository.refresh(session, updated_user)
#     return updated_user


# async def delete_user(session: AsyncSession, user_id: int):
#     user = await repository.get_user_by_id(session, user_id)

#     if not user:
#         raise HTTPException(status_code=404, detail="User does not exists")

#     await repository.delete_user(session, user)
#     await repository.save(session)
#     return True
