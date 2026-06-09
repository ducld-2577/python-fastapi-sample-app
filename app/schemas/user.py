from pydantic import BaseModel


class UserUpdate(BaseModel):
    name: str


class UserOut(BaseModel):
    id: int
    name: str
