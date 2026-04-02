from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User

async def create_user(db: AsyncSession, data):
    user = User(**data.dict())
    db.add(user)
    await db.commit()
    return user
