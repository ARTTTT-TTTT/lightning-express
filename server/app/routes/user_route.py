from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.models import User
from app.schemas.user_schema import UserOut
from app.schemas.user_address_schema import UserAddressOut, UserAddressCreate
from app.crud import user_address_crud as crud
from app.database.session import get_db
from app.security import (
    get_current_user,
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserOut)
async def read_me(current_user: User = Depends(get_current_user)):
    return current_user


# * ====== User Address ======


@router.post("/me/addresses", response_model=UserAddressOut, status_code=status.HTTP_201_CREATED)
async def add_user_address(
    address: UserAddressCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    new_address = await crud.create_user_address(db, getattr(current_user, "id"), address)
    return new_address


@router.get("/me/addresses", response_model=List[UserAddressOut])
async def get_my_addresses(
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    addresses = await crud.get_user_addresses(db, getattr(current_user, "id"))
    return addresses


@router.put("/me/addresses/{address_id}/set_default", response_model=UserOut)
async def set_my_default_address(
    address_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    updated_user = await crud.set_default_address(db, current_user, address_id)
    if not updated_user:
        raise HTTPException(status_code=404, detail="Address not found or does not belong to user")
    return updated_user


@router.delete("/me/addresses/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_my_address(
    address_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    success = await crud.delete_user_address(db, address_id, getattr(current_user, "id"))
    if not success:
        raise HTTPException(status_code=404, detail="Address not found or does not belong to user")
    return
