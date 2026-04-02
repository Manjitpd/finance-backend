from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import require_role
from app.db.session import get_db
from app.schemas.user import UserCreate
from app.services.user_service import create_user, delete_user, get_all_users, get_user_by_id, update_user

router = APIRouter()

@router.post("/")
async def create_user_api(
    data: UserCreate,
    db: AsyncSession = Depends(get_db),
    user=Depends(require_role(["admin"]))
):
    return await create_user(db, data)


@router.get("/")
async def get_users(
    db: AsyncSession = Depends(get_db),
    user=Depends(require_role(["admin"]))
):
    return await get_all_users(db)


@router.get("/{user_id}")
async def get_user(
    user_id: str,
    db: AsyncSession = Depends(get_db),
    user=Depends(require_role(["admin"]))
):
    result = await get_user_by_id(db, user_id)

    if not result:
        return {"error": "User not found"}

    return result


@router.put("/{user_id}")
async def update_user_api(
    user_id: str,
    data: UserCreate,
    db: AsyncSession = Depends(get_db),
    user=Depends(require_role(["admin"]))
):
    updated_user = await update_user(db, user_id, data)

    if not updated_user:
        return {"error": "User not found"}

    return {"message": "User updated successfully"}


@router.delete("/{user_id}")
async def delete_user_api(
    user_id: str,
    db: AsyncSession = Depends(get_db),
    user=Depends(require_role(["admin"]))
):
    success = await delete_user(db, user_id)

    if not success:
        return {"error": "User not found"}

    return {"message": "User deleted successfully"}