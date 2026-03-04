from fastapi import APIRouter , Depends , HTTPException , Form
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from db_main import SessionLocal
from models.company import Company
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

@router.post("/signup-company")
def signup(email: EmailStr = Form(...),company_name: str = Form(...), 
    password: str = Form(...), 
    confirmPassword: str = Form(...),db: Session = Depends(get_db)):

    try:
        #input done
        if len(password) < 8 or len(password) > 72:
            raise HTTPException(status_code = 400 , detail ="password between 8 and 72 characters")
        if password != confirmPassword:
            raise HTTPException(status_code = 400 , detail ="password != confirm password ")

        if(db.query(Company).filter(Company.email == email).first()):
            raise HTTPException(status_code=400, detail="Email already registered")
        if db.query(Company).filter(Company.company_name == company_name).first():
            raise HTTPException(status_code=400, detail="Company name already taken")

        hashed_pw = pwd_context.hash(password)
        new_company = Company(email=email, company_name=company_name, password=hashed_pw)

        db.add(new_company)
        db.commit()
        db.refresh(new_company)
        print(f"--- DATABASE SUCCESS: Created {new_company.company_name} with ID {new_company.id} ---")
        return {"message": "Company created successfully", "company_id": new_company.id}

    except Exception as e:
        db.rollback()
        print(f"!!! DATABASE ERROR !!!: {str(e)}") 
        raise HTTPException(status_code=500, detail=f"System error: {str(e)}")

