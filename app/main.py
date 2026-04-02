from fastapi import FastAPI
from app.api.routes import auth, users, finance, dashboard
from app.db.base import Base
from app.db.session import engine
from fastapi.middleware.cors import CORSMiddleware 



app = FastAPI(title="Finance Dashboard API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(finance.router, prefix="/records", tags=["Finance"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)