from pydantic import BaseModel


class RoomAddSchema(BaseModel):
    name: str
    capacity: int


class RoomSchema(RoomAddSchema):
    id: int

