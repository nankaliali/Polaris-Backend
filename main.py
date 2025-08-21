from contextlib import asynccontextmanager
from fastapi import FastAPI
from api.v1 import auth_routes
from core.database import engine
from api.v1 import drive_data
from api.v1 import test_data
from sqlalchemy.orm import Session
from core.database import SessionLocal, engine, Base

from fastapi.middleware.cors import CORSMiddleware

from core.security import hash_password
from models.drive_data_model import Base
from repository.user_repository import create_user, get_user_by_username
from schemas.user_schema import UserCreate

@asynccontextmanager
async def lifespan(app: FastAPI):
    # — Startup logic —
    # 1) create tables if they don't exist
    Base.metadata.create_all(bind=engine)

    # 2) ensure default admin
    db: Session = SessionLocal()
    try:
        username = "admin@polaris"
        device_id = "admin@polaris"
        password = "admin@polaris"
        pw_hash = hash_password(password)

        existing = get_user_by_username(db, username)
        if not existing:
            create_user(db, username, pw_hash, device_id)
            print(f"✔️   Created default admin user: {username}")
    finally:
        db.close()

    yield  # === your app runs here ===

    # — Shutdown logic (optional) —
    # (nothing to clean up right now)

app = FastAPI(lifespan=lifespan)

app.include_router(auth_routes.router)
app.include_router(drive_data.router)
app.include_router(test_data.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)