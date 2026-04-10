from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db_main import SessionLocal
from models.user import User
from functionalities.auth import get_curr_user_id
from typing import Optional
from pydantic import BaseModel
from passlib.context import CryptContext
router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None

class PassChange(BaseModel):
    current_password: str
    new_password: str

@router.get("/me")
def get_me(user_id: int = Depends(get_curr_user_id), db: Session = Depends(get_db)): # FastAPI pauses get_me and runs get_curr_user_id first.
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        #"phone": user.phone,
        #"location": user.location
    }


@router.put("/me") # change pass 
def update_me(user_data: UserUpdate, user_id: int = Depends(get_curr_user_id), db: Session = Depends(get_db)):
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user_data.first_name is not None:
        user.first_name = user_data.first_name
    if user_data.last_name is not None:
        user.last_name = user_data.last_name
    if user_data.username is not None:
        user.username = user_data.username
    if user_data.email is not None:
        user.email = user_data.email
    db.commit()
    db.refresh(user)
    return {
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
    }


@router.post("/me/change-password")
def change_password(user_data: PassChange, user_id: int = Depends(get_curr_user_id), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(user_data.current_password, user.password):
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    
    if len(user_data.new_password) < 8:
        raise HTTPException(status_code=400, detail="Password must be >= 8")
    
    if user_data.current_password == user_data.new_password:
        raise HTTPException(status_code=400, detail="New password must differ from current")
    
    user.password = get_password_hash(user_data.new_password)
    db.commit()

    return {"message": "Password changed successfully"}