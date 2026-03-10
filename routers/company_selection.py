from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db_main import SessionLocal
from models.company import Company
from models.Recyclables import Recyclable_Item
from pydantic import BaseModel

router = APIRouter()


# ─── DB Dependency ────────────────────────────────────────────────────────────
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ─── Schemas ──────────────────────────────────────────────────────────────────
class AssignCompanyRequest(BaseModel):
    company_id: int


# ─── GET /companies ───────────────────────────────────────────────────────────
# Returns all registered companies so the user can pick one.
@router.get("/companies")
def list_companies(db: Session = Depends(get_db)):
    """
    Returns all companies available for selection.
    Called by the frontend company-picker page.
    """
    companies = db.query(Company).all()
    return [
        {
            "id":           c.id,
            "company_name": c.company_name,
            "email":        c.email,
        }
        for c in companies
    ]


# ─── POST /items/{item_id}/assign-company ─────────────────────────────────────
# The authenticated user assigns a company to one of their recyclable items.
@router.post("/items/{item_id}/assign-company")
def assign_company(
    item_id: int,
    body: AssignCompanyRequest,
    db: Session = Depends(get_db),
    # TODO: swap the line below for your real JWT/session auth dependency
    # current_user: User = Depends(get_current_user),
):
    """
    Assigns a company to a specific recyclable item that belongs to the user.
    Changes the item's status from 'pending' → 'assigned'.
    """
    # ── 1. Validate the item exists ──────────────────────────────────────────
    item = db.query(Recyclable_Item).filter(Recyclable_Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Recyclable item not found")

    # ── 2. Ownership check (uncomment when auth is wired up) ─────────────────
    # if item.user_id != current_user.id:
    #     raise HTTPException(status_code=403, detail="Not your item")

    # ── 3. Validate the company exists ───────────────────────────────────────
    company = db.query(Company).filter(Company.id == body.company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    # ── 4. Guard: don't re-assign already collected items ────────────────────
    if item.status == "collected":
        raise HTTPException(
            status_code=400,
            detail="Cannot reassign an item that has already been collected"
        )

    # ── 5. Persist ───────────────────────────────────────────────────────────
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


# ─── GET /items/{item_id}/assigned-company ────────────────────────────────────
# Lets the frontend check which company is currently assigned to an item.
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