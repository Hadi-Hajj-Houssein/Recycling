from fastapi import APIRouter , Depends , HTTPException , Form
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from db_main import SessionLocal
from models.user import User
from models.company import Company
router = APIRouter()
hash = CryptContext(schemes=["bcrypt"], deprecated = "auto")

 

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login")
def login(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    # Check users table first
    user = db.query(User).filter(User.email == username).first()
    if user:
        if not hash.verify(password, user.password):
            raise HTTPException(status_code=400, detail="Invalid email or password")
        return {"message": "Login successful", "user_id": user.id, "role": "user"}

    # Check companies table
    company = db.query(Company).filter(Company.email == username).first()
    if company:
        if not hash.verify(password, company.password):
            raise HTTPException(status_code=400, detail="Invalid email or password")
        return {"message": "Login successful", "company_id": company.id, "role": "company"}

    raise HTTPException(status_code=400, detail="Invalid email or password")



