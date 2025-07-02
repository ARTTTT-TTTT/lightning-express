from pydantic import BaseModel, EmailStr
from uuid import UUID


class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserOut(UserBase):
    id: UUID

    model_config = {"from_attributes": True}
