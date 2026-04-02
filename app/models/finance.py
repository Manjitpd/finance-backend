from sqlalchemy import Column, String, Float, Date, Text, Boolean
from app.db.base import Base
import uuid

class FinanceRecord(Base):
    __tablename__ = "finance_records"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    amount = Column(Float)
    type = Column(String)
    category = Column(String)
    date = Column(Date)
    notes = Column(Text)
    created_by = Column(String)
    is_deleted = Column(Boolean, default=False)