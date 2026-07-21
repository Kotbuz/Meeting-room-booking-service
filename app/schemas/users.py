from pydantic import BaseModel


class UserAddSchema(BaseModel):
    login: str
    password: str
    role: str


class UserSchema(UserAddSchema):
    id: int
