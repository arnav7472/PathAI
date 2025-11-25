from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from models.users import UserRegister, UserLogin, Token, UserResponse
from utils.password_hasher import get_password_hash, verify_password
from utils.jwt_handler import create_access_token, verify_token
from core.database import get_supabase
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["authentication"])
security = HTTPBearer()

# In-memory database (replace with Supabase later)
users_db = []
next_id = 1

def get_user_by_email(email: str):
    for user in users_db:
        if user['email'] == email:
            return user
    return None

def get_user_by_id(user_id: int):
    for user in users_db:
        if user['id'] == user_id:
            return user
    return None

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        user_id = verify_token(credentials.credentials)
        user = get_user_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )

@router.post("/register", response_model=dict)
async def register(user_data: UserRegister):
    global next_id
    
    if get_user_by_email(user_data.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    if len(user_data.password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters")
    
    hashed_password = get_password_hash(user_data.password)
    
    new_user = {
        "id": next_id,
        "name": user_data.name,
        "email": user_data.email,
        "hashed_password": hashed_password,
        "is_active": True
    }
    users_db.append(new_user)
    next_id += 1
    
    access_token = create_access_token(data={"sub": new_user['id']})
    
    return {
        "status": "success",
        "message": "User registered successfully",
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": new_user['id'],
        "user": {
            "id": new_user['id'],
            "name": new_user['name'],
            "email": new_user['email']
        }
    }

@router.post("/login", response_model=dict)
async def login(login_data: UserLogin):
    user = get_user_by_email(login_data.email)
    
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    if not verify_password(login_data.password, user['hashed_password']):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    access_token = create_access_token(data={"sub": user['id']})
    
    return {
        "status": "success",
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user['id'],
        "user": {
            "id": user['id'],
            "name": user['name'],
            "email": user['email']
        }
    }

@router.get("/me", response_model=dict)
async def get_current_user_profile(current_user: dict = Depends(get_current_user)):
    return {
        "status": "success",
        "user": {
            "id": current_user['id'],
            "name": current_user['name'],
            "email": current_user['email'],
            "is_active": current_user['is_active']
        }
    }