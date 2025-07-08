# schemas/user_schema.py
from pydantic import BaseModel, EmailStr, model_validator, field_validator, Field
from typing import Optional, List
from datetime import datetime
import re

from app.models import UserTypeEnum
from app.schemas.user_address_schema import UserAddressOut


class UserBase(BaseModel):
    username: str
    email: Optional[EmailStr] = Field(default=None)
    full_name: Optional[str] = Field(default=None)
    phone_number: Optional[str] = Field(default=None)
    user_type: UserTypeEnum = UserTypeEnum.CUSTOMER


class UserCreate(UserBase):
    password: str

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        if not re.fullmatch(r"[a-z0-9]+", v):
            raise ValueError(
                "Username must contain only lowercase letters and numbers, no spaces or special characters"
            )
        return v.strip().lower()

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: Optional[str]) -> Optional[str]:
        return v.strip().lower() if v else v

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        if not re.fullmatch(r"[0-9]{7,20}", v):
            raise ValueError(
                "Phone number must contain digits only (7-20 characters), no spaces or symbols"
            )
        return v.strip()

    @model_validator(mode="after")
    def check_email_or_phone_number(self) -> "UserCreate":
        if not self.email and not self.phone_number:
            raise ValueError("Either email or phone_number must be provided.")
        return self


class UserOut(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    addresses: List[UserAddressOut] = []
    default_address: Optional[UserAddressOut]

    model_config = {"from_attributes": True}
