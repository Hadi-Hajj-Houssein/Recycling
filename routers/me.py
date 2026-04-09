from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db_main import SessionLocal
from models.user import User
from functionalities.auth import get_curr_user_id
from typing import Optional
from pydantic import BaseModel
router = APIRouter()

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


@router.put("/me")
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