from typing import Optional
from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    role: str

class UserUpdate(BaseModel):
    name: str
    email: str
    role: str
    password: Optional[str] = None 

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    role: str
    is_active: Optional[bool] = True