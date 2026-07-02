from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from pydantic import EmailStr, BaseModel
import smtplib
import random
from email.mime.text import MIMEText
from db_main import SessionLocal
from models.user import User
from models.company import Company
from email_verification import SENDER_EMAIL, APP_PASSWORD

router = APIRouter()
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

verification_codes = {}

class EmailRequest(BaseModel):
    email: EmailStr

class VerifyRequest(BaseModel):
    email: EmailStr
    code: str

@router.post("/signup-user")
def signup(
    email: EmailStr = Form(...),
    username: str = Form(...),
    password: str = Form(...),
    confirmPassword: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        if len(password) < 8 or len(password) > 72:
            raise HTTPException(status_code=400, detail="password between 8 and 72 characters")

        if password != confirmPassword:
            raise HTTPException(status_code=400, detail="password != confirm password")

        if db.query(User).filter(User.email == email).first():
            raise HTTPException(status_code=400, detail="Email already registered")

        if db.query(User).filter(User.username == username).first():
            raise HTTPException(status_code=400, detail="Username already taken")

        if db.query(Company).filter(Company.email == email).first():
            raise HTTPException(status_code=400, detail="Email already registered as a company")

        hashed_pw = pwd_context.hash(password)
        new_user = User(email=email, username=username, password=hashed_pw, amount=0.0)

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        print(f"✅ User created: {new_user.username} (ID: {new_user.id})")
        return {"message": "User created successfully", "user_id": new_user.id}

    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        print(f"❌ Database error: {str(e)}")
        raise HTTPException(status_code=500, detail="System error")

@router.post("/send-code")
def send_code(data: EmailRequest):
    code = str(random.randint(100000, 999999))
    verification_codes[data.email] = code

    msg = MIMEText(f"Your EcoCollect verification code is: {code}")
    msg["Subject"] = "Your Verification Code"
    msg["From"]    = SENDER_EMAIL
    msg["To"]      = data.email

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.sendmail(SENDER_EMAIL, data.email, msg.as_string())
        server.quit()
        return {"message": "Verification code sent"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Email sending failed: {str(e)}")

@router.post("/verify-code")
def verify_code(data: VerifyRequest):
    saved_code = verification_codes.get(data.email)
    if not saved_code:
        raise HTTPException(status_code=404, detail="No code found. Request a new one.")
    if saved_code != data.code:
        raise HTTPException(status_code=400, detail="Wrong code. Please try again.")
    del verification_codes[data.email]
    return {"message": "Email verified successfully"}