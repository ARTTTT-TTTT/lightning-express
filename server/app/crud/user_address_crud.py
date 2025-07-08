from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import User, UserAddress
from app.schemas.user_address_schema import UserAddressCreate


async def create_user_address(
    db: AsyncSession, user_id: int, address: UserAddressCreate
) -> UserAddress:
    db_address = UserAddress(
        user_id=user_id,
        address_line=address.address_line,
        subdistrict=address.subdistrict,
        district=address.district,
        province=address.province,
        postal_code=address.postal_code,
        phone_number=address.phone_number,
        address_type=address.address_type,
    )
    db.add(db_address)
    await db.commit()
    await db.refresh(db_address)
    return db_address


async def get_user_addresses(db: AsyncSession, user_id: int) -> list[UserAddress]:
    result = await db.execute(select(UserAddress).filter(UserAddress.user_id == user_id))
    return list(result.scalars().all())


async def get_user_address_by_id(
    db: AsyncSession, address_id: int, user_id: int
) -> UserAddress | None:
    result = await db.execute(
        select(UserAddress).filter(UserAddress.id == address_id, UserAddress.user_id == user_id)
    )
    return result.scalars().first()


async def set_default_address(db: AsyncSession, user: User, address_id: int) -> User | None:
    user_id = getattr(user, "id", None)
    if not isinstance(user_id, int):
        return None
    address = await get_user_address_by_id(db, address_id, user_id)
    if not address:
        return None

    setattr(user, "default_address_id", address_id)
    await db.commit()
    await db.refresh(user)
    return user


async def delete_user_address(db: AsyncSession, address_id: int, user_id: int) -> bool:
    address = await get_user_address_by_id(db, address_id, user_id)
    if not address:
        return False

    if user_id == address.user_id and address_id == address.user.default_address_id:
        address.user.default_address_id = None
        await db.commit()

    await db.delete(address)
    await db.commit()
    return True
