from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import require_role
from app.db.session import get_db
from app.schemas.user import UserCreate
from app.services.user_service import create_user

router = APIRouter()

@router.post("/")
async def create_user_api(
    data: UserCreate,
    db: AsyncSession = Depends(get_db),
    user=Depends(require_role(["admin"]))
):
    return await create_user(db, data)