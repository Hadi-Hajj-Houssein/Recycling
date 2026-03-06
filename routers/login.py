from fastapi import APIRouter , Depends , HTTPException , Form
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from db_main import SessionLocal
from models.user import User
router = APIRouter()
hash = CryptContext(schemes=["bcrypt"], deprecated = "auto")

from functionalities.auth import create_access_token

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login")
def login(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == username).first()
    if not user:
        raise HTTPException(status_code = 400, detail = "Invalid email or password")
    
    access_token  = create_access_token(sub = str(user.id),expires_minutes = 15)
    return{
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "amount": user.amount
        }
    }



