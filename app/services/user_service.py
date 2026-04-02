from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User

async def create_user(db: AsyncSession, data):
    user = User(**data.dict())
    db.add(user)
    await db.commit()
    return user


async def get_all_users(db: AsyncSession):
    result = await db.execute(select(User))
    return result.scalars().all()


async def get_user_by_id(db: AsyncSession, user_id: str):
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalars().first()


async def update_user(db: AsyncSession, user_id: str, data):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()

    if not user:
        return None

    user.name = data.name
    user.email = data.email
    user.password = data.password
    user.role = data.role

    await db.commit()
    await db.refresh(user)
    return user


async def delete_user(db: AsyncSession, user_id: str):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()

    if not user:
        return None

    await db.delete(user)
    await db.commit()
    return True