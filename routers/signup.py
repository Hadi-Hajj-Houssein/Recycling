from fastapi import APIRouter , Depends , HTTPException , Form
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from db_main import SessionLocal
from models.user import User
router = APIRouter()
hash = CryptContext(schemes=["bcrypt"], deprecated = "auto")
from pydantic import EmailStr

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/signup")
def signup(email: EmailStr = Form(...),username: str = Form(...), 
    password: str = Form(...), 
    confirmPassword: str = Form(...),db: Session = Depends(get_db)):


    #input done 
    if len(password) < 8:
        raise HTTPException(status_code = 400 , detail ="password short   < 8 ")
    if password != confirmPassword:
        raise HTTPException(status_code = 400 , detail ="password != confirm password ")

    if(db.query(User).filter(User.email == email).first()):
        raise HTTPException(status_code=400, detail="Email already registered")
    if db.query(User).filter(User.username == username).first():
        raise HTTPException(status_code=400, detail="Username already taken")

    hashed_pw = pwd_context.hash(password)
    new_user = User(email=email, username=username, password=hashed_pw, amount=0.0)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully", "user_id": new_user.id}


