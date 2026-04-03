from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.models.user import User
from app.core.security import create_access_token
from app.services.user_service import get_user_by_email

router = APIRouter()

@router.post("/login")
async def login(email: str, password: str, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_email(db, email)

    if not user or user.password != password:
        return {"error": "Invalid credentials"}

    token = create_access_token({"id": user.id, "role": user.role})
    return {"access_token": token}