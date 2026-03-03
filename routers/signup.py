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

    try:
        #input done
        if len(password) < 8 or len(password) > 72:
            raise HTTPException(status_code = 400 , detail ="password between 8 and 72 characters")
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
        print(f"--- DATABASE SUCCESS: Created {new_user.username} with ID {new_user.id} ---")
        return {"message": "User created successfully", "user_id": new_user.id}

    except Exception as e:
        db.rollback()
        print(f"!!! DATABASE ERROR !!!: {str(e)}") # LOOK AT YOUR TERMINAL FOR THIS
        raise HTTPException(status_code=500, detail=f"System error: {str(e)}")

