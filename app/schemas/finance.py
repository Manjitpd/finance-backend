from pydantic import BaseModel
from datetime import date

class FinanceCreate(BaseModel):
    amount: float
    type: str
    category: str
    date: date
    notes: str | None = None