from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
import uuid

async def create_user(db: AsyncSession, data):
    """Create a new user and return a dictionary"""
    # Check if user already exists
    result = await db.execute(select(User).where(User.email == data.email))
    existing_user = result.scalars().first()
    
    if existing_user:
        return {"error": "User with this email already exists"}
    
    # Create new user
    user = User(
        id=str(uuid.uuid4()),
        name=data.name,
        email=data.email,
        password=data.password,  # In production, hash this!
        role=data.role,
        is_active=True
    )
    
    db.add(user)
    await db.commit()
    await db.refresh(user)
    
    # Return a dictionary instead of SQLAlchemy object
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "is_active": user.is_active
    }

async def get_all_users(db: AsyncSession):
    """Get all users as dictionaries"""
    result = await db.execute(select(User))
    users = result.scalars().all()
    
    return [
        {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "is_active": user.is_active
        }
        for user in users
    ]

async def get_user_by_id(db: AsyncSession, user_id: str):
    """Get a single user by ID as dictionary"""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()

    if not user:
        return None

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "is_active": user.is_active
    }

async def update_user(db: AsyncSession, user_id: str, data):
    """Update a user"""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()

    if not user:
        return None

    user.name = data.name
    user.email = data.email
    if data.password:  # Only update password if provided
        user.password = data.password  # In production, hash this!
    user.role = data.role

    await db.commit()
    await db.refresh(user)
    
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "is_active": user.is_active
    }

async def delete_user(db: AsyncSession, user_id: str):
    """Delete a user"""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()

    if not user:
        return None

    await db.delete(user)
    await db.commit()
    return True