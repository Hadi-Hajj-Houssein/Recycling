from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db_main import SessionLocal
from models.user import User
from functionalities.auth import get_curr_user_id

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/me")
def get_me(user_id: int = Depends(get_curr_user_id), db: Session = Depends(get_db)): # FastAPI pauses get_me and runs get_curr_user_id first.
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "username": user.username,
        "email": user.email
    }