from pydantic import BaseModel

from app.core.roles import UserRole


class UserCreateSchema(BaseModel):
    login: str
    password: str


class UserResponseSchema(BaseModel):
    id: int
    login: str
    role: UserRole


class UserUpdateSchema(BaseModel):
    login: str | None = None
    password: str | None = None
    role: UserRole | None = None


class UserLoginSchema(BaseModel):
    login: str
    password: str


class TokenSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"
