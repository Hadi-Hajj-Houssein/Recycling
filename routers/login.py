from fastapi import APIRouter, Depends, HTTPException, Form, Response
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from db_main import SessionLocal
from models.user import User
from models.company import Company
from functionalities.auth import create_access_token

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def set_auth_cookie(response: Response, token: str):
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax",
        secure=False,
        path="/",
        max_age=7200  # 2 hours
        # NO domain= here — let the browser infer localhost
    )

@router.post("/login")
def login(
    response: Response,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == email).first()
    if user and pwd_context.verify(password, user.password):
        token = create_access_token(
            data={"sub": str(user.id), "role": "user"},
            expires_minutes=120
        )
        set_auth_cookie(response, token)
        return {"role": "user", "user_id": user.id}

    company = db.query(Company).filter(Company.email == email).first()
    if company and pwd_context.verify(password, company.password):
        token = create_access_token(
            data={"sub": str(company.id), "role": "company"},
            expires_minutes=120
        )
        set_auth_cookie(response, token)
        return {"role": "company", "company_id": company.id}

    raise HTTPException(status_code=401, detail="Invalid email or password")