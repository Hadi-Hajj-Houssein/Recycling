from fastapi import APIRouter, Depends, HTTPException, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from db_main import SessionLocal
from models.user import User
from models.company import Company
router = APIRouter()
#hash = CryptContext(schemes=["bcrypt"], deprecated = "auto")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
from functionalities.auth import create_access_token

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login")
def login(email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if user and pwd_context.verify(password, user.password):
        token = create_access_token(
            data={"sub": str(user.id), "role": "user"},
            expires_minutes=15
        )
        print (token)
        return {
            "access_token": token,
            "token_type": "bearer",
            "role": "user",
            "user_id": user.id
        }
    company = db.query(Company).filter(Company.email == email).first()
    if company and pwd_context.verify(password, company.password):
    
        token = create_access_token(
        data={"sub": str(company.id), "role": "company"},
        expires_minutes=15
        )
        return {
            "access_token": token,
            "token_type": "bearer",
            "role": "company",
            "company_id": company.id
        }
    raise HTTPException(status_code=401, detail="Invalid email or password")



