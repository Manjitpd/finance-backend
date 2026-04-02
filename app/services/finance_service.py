from sqlalchemy import select
from app.models.finance import FinanceRecord
from sqlalchemy.ext.asyncio import AsyncSession


async def get_filtered_records(db, type, category, start_date, end_date, page, limit):
    query = select(FinanceRecord).where(FinanceRecord.is_deleted == False)

    if type:
        query = query.where(FinanceRecord.type == type)

    if category:
        query = query.where(FinanceRecord.category == category)

    if start_date:
        query = query.where(FinanceRecord.date >= start_date)

    if end_date:
        query = query.where(FinanceRecord.date <= end_date)    

    query = query.offset((page - 1) * limit).limit(limit)

    result = await db.execute(query)
    return result.scalars().all()


async def create_record_service(db: AsyncSession, data, user_id: str):
    record = FinanceRecord(**data.dict(), created_by=user_id)
    db.add(record)
    await db.commit()
    await db.refresh(record)
    return record


async def update_record_service(db: AsyncSession, id: str, data):
    result = await db.execute(
        select(FinanceRecord).where(
            FinanceRecord.id == id,
            FinanceRecord.is_deleted == False
        )
    )
    record = result.scalars().first()

    if not record:
        return None

    record.amount = data.amount
    record.type = data.type
    record.category = data.category
    record.date = data.date
    record.notes = data.notes

    await db.commit()
    return record



async def delete_record_service(db: AsyncSession, id: str):
    result = await db.execute(
        select(FinanceRecord).where(
            FinanceRecord.id == id,
            FinanceRecord.is_deleted == False
        )
    )
    record = result.scalars().first()

    if not record:
        return None

    record.is_deleted = True
    await db.commit()
    return True
