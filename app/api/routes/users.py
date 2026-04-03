from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import require_role
from app.db.session import get_db
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.services.user_service import create_user, delete_user, get_all_users, get_user_by_email, get_user_by_id, update_user
from typing import List

router = APIRouter()

@router.post("/", response_model=UserResponse)
async def create_user_api(
    data: UserCreate,
    db: AsyncSession = Depends(get_db),
    user = Depends(require_role(["admin"]))
):
    exiting_user = await get_user_by_email(db, data.email)
    if exiting_user:
        raise HTTPException(status_code=400, detail="User with this email already exists")
    
    result = await create_user(db, data)
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result

@router.get("/", response_model=List[UserResponse])
async def get_users(
    db: AsyncSession = Depends(get_db),
    user = Depends(require_role(["admin"]))
):
    return await get_all_users(db)

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    db: AsyncSession = Depends(get_db),
    user = Depends(require_role(["admin"]))
):
    result = await get_user_by_id(db, user_id)

    if not result:
        raise HTTPException(status_code=404, detail="User not found")

    return result

@router.put("/{user_id}")
async def update_user_api(
    user_id: str,
    data: UserUpdate,
    db: AsyncSession = Depends(get_db),
    user = Depends(require_role(["admin"]))
):
    updated_user = await update_user(db, user_id, data)

    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "User updated successfully", "user": updated_user}

@router.delete("/{user_id}")
async def delete_user_api(
    user_id: str,
    db: AsyncSession = Depends(get_db),
    user = Depends(require_role(["admin"]))
):
    success = await delete_user(db, user_id)

    if not success:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "User deleted successfully"}