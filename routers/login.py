from fastapi import APIRouter, Depends, HTTPException, Form, Response
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import re
from db_main import SessionLocal
from models.user import User
from models.company import Company
from functionalities.auth import create_access_token

router = APIRouter()
pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")

TOKEN_EXPIRE_MINUTES = 120

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def validate_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def set_auth_cookie(response: Response, token: str):
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax",
        secure=False,
        path="/",
        max_age=TOKEN_EXPIRE_MINUTES * 60
    )

@router.post("/login")
def login(
    response: Response,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    email = email.strip().lower()
    if not validate_email(email):
        raise HTTPException(status_code=400, detail="Invalid email format")
    
    if not password or len(password) < 6:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    password = password[:72]
    
    user = db.query(User).filter(User.email == email).first()
    if user and pwd_context.verify(password, user.password):
        token = create_access_token(
            data={
                "sub": str(user.id),
                "role": "user"
            },
            expires_minutes=TOKEN_EXPIRE_MINUTES
        )
        set_auth_cookie(response, token)
        return {
            "role": "user",
            "user_id": user.id,
            "name": user.name if hasattr(user, 'name') else "User",
            "message": "Logged in as user"
        }

    company = db.query(Company).filter(Company.email == email).first()
    if company and pwd_context.verify(password, company.password):
        token = create_access_token(
            data={
                "sub": str(company.id),
                "role": "company"
            },
            expires_minutes=TOKEN_EXPIRE_MINUTES
        )
        set_auth_cookie(response, token)
        return {
            "role": "company",
            "company_id": company.id,
            "name": company.name if hasattr(company, 'name') else company.company_name if hasattr(company, 'company_name') else "Company",
            "message": "Logged in as company"
        }
    
    raise HTTPException(
        status_code=401,
        detail="Invalid email or password"
    )