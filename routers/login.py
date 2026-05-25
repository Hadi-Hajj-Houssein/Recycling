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
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

TOKEN_EXPIRE_MINUTES = 120

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def validate_email(email: str) -> bool:
    """✅ Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def set_auth_cookie(response: Response, token: str):
    """✅ Set secure HTTP-only cookie"""
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,  # ✅ Can't be stolen by JavaScript (XSS protection)
        samesite="lax",  # ✅ CSRF protection
        secure=False,  # Change to True for HTTPS production
        path="/",
        max_age=TOKEN_EXPIRE_MINUTES * 60  # 2 hours
    )

@router.post("/login")
def login(
    response: Response,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    ✅ Secure login endpoint for both USER and COMPANY
    - Email validation
    - Password hashing verification
    - HTTP-only cookie with token
    - Generic error messages (security)
    """
    
    # ✅ 1. Validate email format
    email = email.strip().lower()
    if not validate_email(email):
        raise HTTPException(status_code=400, detail="Invalid email format")
    
    # ✅ 2. Validate password not empty
    if not password or len(password) < 6:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    # ✅ 3. Check USER table first
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

    # ✅ 4. Check COMPANY table
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
    
    # ✅ 5. Generic error message (don't reveal if email exists)
    raise HTTPException(
        status_code=401,
        detail="Invalid email or password"
    )