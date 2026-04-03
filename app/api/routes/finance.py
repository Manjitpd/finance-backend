from datetime import date
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.finance import FinanceCreate
from app.services.finance_service import create_record_service, delete_record_service, get_filtered_records, update_record_service
from app.api.deps import require_role

router = APIRouter()

@router.post("/")
async def create_record(
    data: FinanceCreate,
    db: AsyncSession = Depends(get_db),
    user=Depends(require_role(["admin"]))
):
    return await create_record_service(db, data, user["id"])


@router.get("/")
async def get_records(
    type: str | None = None,
    category: str | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
    page: int = 1,
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
    user=Depends(require_role(["admin", "analyst"])) 
):
    return await get_filtered_records(
        db, type, category, start_date, end_date, page, limit
    )


@router.put("/{id}")
async def update_record(
    id: str,
    data: FinanceCreate,
    db: AsyncSession = Depends(get_db),
    user=Depends(require_role(["admin"]))
):
    record = await update_record_service(db, id, data)

    if not record:
        return {"error": "Record not found"}

    return {"message": "Record updated successfully"}

@router.delete("/{id}")
async def delete_record(
    id: str,
    db: AsyncSession = Depends(get_db),
    user=Depends(require_role(["admin"]))
):
    success = await delete_record_service(db, id)

    if not success:
        return {"error": "Record not found"}

    return {"message": "Record deleted successfully"}