from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db_main import SessionLocal
from models.company import Company
from models.Recyclables import Recyclable_Item
from pydantic import BaseModel
from functionalities.auth import get_curr_company_id
router = APIRouter()

from routers.dependencies import get_db

class AssignCompanyRequest(BaseModel):
    company_id: int


@router.get("/companies")
def list_companies(db: Session = Depends(get_db)):

    companies = db.query(Company).all()
    return [
        {
            "id":           c.id,
            "company_name": c.company_name,
            "email":        c.email,
        }
        for c in companies
    ]



@router.post("/items/{item_id}/assign-company")
def assign_company(
    item_id: int,
    body: AssignCompanyRequest,
    db: Session = Depends(get_db),
):
    
    item = db.query(Recyclable_Item).filter(Recyclable_Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Recyclable item not found")

    company = db.query(Company).filter(Company.id == body.company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    if item.status == "collected":
        raise HTTPException(
            status_code=400,
            detail="Cannot reassign an item that has already been collected"
        )

    item.company_id = body.company_id
    item.status     = "assigned"
    db.commit()
    db.refresh(item)

    return {
        "message":      "Company assigned successfully",
        "item_id":      item.id,
        "company_id":   item.company_id,
        "company_name": company.company_name,
        "status":       item.status,
    }
@router.get("/items/{item_id}/assigned-company")
def get_assigned_company(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Recyclable_Item).filter(Recyclable_Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if not item.company_id:
        return {"company": None}
    company = db.query(Company).filter(Company.id == item.company_id).first()
    return {
        "company": {
            "id":           company.id,
            "company_name": company.company_name,
            "email":        company.email,
        }
    }

@router.get("/items/{item_id}")
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Recyclable_Item).filter(Recyclable_Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    return {
        "id": item.id,
        "name": item.name,
        "type": item.type,
        "desc": item.desc,
        "weight": item.weight,
        "condition": item.condition,
        "status": item.status,
        "company_id": item.company_id
    }