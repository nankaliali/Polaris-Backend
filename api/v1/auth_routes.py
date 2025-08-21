from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from repository.user_repository import create_user, get_user_by_device_id, get_user_by_username, update_user_password
from schemas.user_schema import UserCreate, UserRead
from core.security import verify_password, hash_password
from core.jwt import create_access_token
from core.database import get_db
from pydantic import BaseModel

import random

def generate_random_password(length: int = 6):
    return ''.join(str(random.randint(0, 9)) for _ in range(length))

# Response model for login that includes both token and user data
class LoginResponse(BaseModel):
    access_token: str
    token_type: str

# Request model for login
class LoginRequest(BaseModel):
    username: str
    password: str

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post(
    "/signup",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
)
def signup(
    user_in: UserCreate,
    db:      Session = Depends(get_db),
):
    # 1) Check if username or device_id is already taken
    if get_user_by_username(db, user_in.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    if get_user_by_device_id(db, user_in.device_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Device ID already registered",
        )

    # 2) Hash the password
    pw_hash = hash_password(user_in.password)

    # 3) Create the user (now including device_id)
    new_user = create_user(
        db,
        username=user_in.username,
        hashed_password=pw_hash,
        device_id=user_in.device_id,
    )

    return new_user

@router.post("/login", response_model=LoginResponse)
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """Login endpoint that returns both access token and user object"""
    db_user = get_user_by_username(db, login_data.username)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Username does not exist"
        )
    if not verify_password(login_data.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Password is incorrect"
        )
    
    access_token = create_access_token({"username": db_user.username})
    
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
    )

# Alternative: Simple login endpoint that accepts form data or query parameters
@router.post("/login-simple")
def login_simple(
    username: str, 
    password: str, 
    db: Session = Depends(get_db)
):
    """Simple login endpoint with query/form parameters (your original style)"""
    db_user = get_user_by_username(db, username)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Username does not exist"
        )
    if not verify_password(password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Password is incorrect"
        )
    
    access_token = create_access_token({"username": db_user.username})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": db_user  # This will be automatically serialized by FastAPI
    }

@router.post("/change-password-random")
def change_password_random(
    username: str,
    db: Session = Depends(get_db)
):
    db_user = get_user_by_username(db, username)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Username does not exist"
        )
    new_password = generate_random_password(6)
    new_hashed_pwd = hash_password(new_password)
    updated_user = update_user_password(db, username, new_hashed_pwd)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Password update failed due to server error"
        )
    return {"username": username, "new_password": new_password}


@router.get("/check-username-simple/{username}")
def check_username_simple(
    username: str,
    db: Session = Depends(get_db)
):
    """Simple username check that returns boolean"""
    db_user = get_user_by_username(db, username)
    return {"username": username, "exists": bool(db_user)}