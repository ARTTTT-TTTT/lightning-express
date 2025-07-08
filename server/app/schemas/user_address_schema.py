from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models import AddressTypeEnum


class UserAddressBase(BaseModel):
    address_line: str
    subdistrict: str
    district: str
    province: str
    postal_code: str
    phone_number: Optional[str] = None
    address_type: AddressTypeEnum = AddressTypeEnum.HOME


class UserAddressCreate(UserAddressBase):
    pass


class UserAddressOut(UserAddressBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
