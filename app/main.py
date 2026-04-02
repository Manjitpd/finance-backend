from fastapi import FastAPI
from app.api.routes import auth, users, finance, dashboard
from app.db.base import Base
from app.db.session import engine

app = FastAPI(title="Finance Dashboard API")

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(finance.router, prefix="/records", tags=["Finance"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)