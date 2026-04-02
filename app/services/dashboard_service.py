from sqlalchemy import select, func, extract
from app.models.finance import FinanceRecord


async def get_summary(db):
    income = await db.execute(
        select(func.sum(FinanceRecord.amount))
        .where(FinanceRecord.type == "income", FinanceRecord.is_deleted == False)
    )

    expense = await db.execute(
        select(func.sum(FinanceRecord.amount))
        .where(FinanceRecord.type == "expense", FinanceRecord.is_deleted == False)
    )

    income_val = income.scalar() or 0
    expense_val = expense.scalar() or 0

    category_result = await db.execute(
        select(
            FinanceRecord.category,
            func.sum(FinanceRecord.amount)
        )
        .where(FinanceRecord.is_deleted == False)
        .group_by(FinanceRecord.category)
    )

    category_data = [
        {"category": row[0], "total": row[1]}
        for row in category_result.all()
    ]

  
    recent_result = await db.execute(
        select(FinanceRecord)
        .where(FinanceRecord.is_deleted == False)
        .order_by(FinanceRecord.date.desc())
        .limit(5)
    )

    recent_data = [
        {
            "amount": r.amount,
            "type": r.type,
            "category": r.category,
            "date": r.date,
            "notes": r.notes
        }
        for r in recent_result.scalars().all()
    ]

    monthly_result = await db.execute(
        select(
            extract("month", FinanceRecord.date).label("month"),
            FinanceRecord.type,
            func.sum(FinanceRecord.amount)
        )
        .where(FinanceRecord.is_deleted == False)
        .group_by("month", FinanceRecord.type)
        .order_by("month")
    )

    monthly_data = {}
    for month, type_, total in monthly_result.all():
        month = int(month)
        if month not in monthly_data:
            monthly_data[month] = {"income": 0, "expense": 0}
        monthly_data[month][type_] = total

    return {
        "summary": {
            "total_income": income_val,
            "total_expense": expense_val,
            "net_balance": income_val - expense_val
        },
        "category_totals": category_data,
        "recent_activity": recent_data,
        "monthly_trends": monthly_data
    }