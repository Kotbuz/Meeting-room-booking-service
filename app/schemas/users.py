from pydantic import BaseModel


class UserCreateSchema(BaseModel):
    login: str
    password: str


class UserResponseSchema(BaseModel):
    id: int
    login: str
    role: str


class UserUpdateSchema(BaseModel):
    login: str | None = None
    password: str | None = None
    role: str | None = None


class UserLoginSchema(BaseModel):
    login: str
    password: str


class TokenSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"
