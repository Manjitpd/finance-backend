from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import require_role
from app.db.session import get_db
from app.services.dashboard_service import get_summary

router = APIRouter()

@router.get("/summary")
async def summary(
    db: AsyncSession = Depends(get_db),
    user=Depends(require_role(["admin", "analyst","viewer"]))
):
    return await get_summary(db)