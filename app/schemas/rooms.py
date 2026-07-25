from pydantic import BaseModel


class RoomCreateSchema(BaseModel):
    name: str
    capacity: int


class RoomSchema(RoomCreateSchema):
    id: int


class RoomResponseSchema(BaseModel):
    id: int
    name: str
    capacity: int


class RoomUpdateSchema(BaseModel):
    name: str | None = None
    capacity: int | None = None
