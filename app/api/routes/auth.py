from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.models.user import User
from app.core.security import create_access_token

router = APIRouter()

@router.post("/login")
async def login(email: str, password: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalars().first()

    if not user or user.password != password:
        return {"error": "Invalid credentials"}

    token = create_access_token({"id": user.id, "role": user.role})
    return {"access_token": token}