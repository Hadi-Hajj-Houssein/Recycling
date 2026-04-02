from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db_main import SessionLocal
from functionalities.auth import get_curr_user_id
from models.user_total_recycled import UserTotalRecycled
from models.Recyclables import Recyclable_Item
router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def calc_pct(value: float, total: float) -> float:
    if total == 0:
        return 0.0
    return round((value / total) * 100, 1) # func bet jib percentage mech aktar 


@router.get("/dashboard")
def dashboard_data(
    user_id: int = Depends(get_curr_user_id),
    db: Session = Depends(get_db)
):
    items = db.query(Recyclable_Item).filter(
        Recyclable_Item.user_id == user_id
    ).all()

    totals = {
        "plastic": 0.0,
        "paper": 0.0,
        "glass": 0.0,
        "metal": 0.0,
        "organic": 0.0,
        "electronics": 0.0
    }

    for item in items:
        if item.type in totals:
            totals[item.type] += item.weight

    total = sum(totals.values())

    def pct(val):
        if total == 0:
            return 0.0
        return round((val / total) * 100, 1)

    return {
        "plastic_pct":     pct(totals["plastic"]),
        "paper_pct":       pct(totals["paper"]),
        "glass_pct":       pct(totals["glass"]),
        "metal_pct":       pct(totals["metal"]),
        "organic_pct":     pct(totals["organic"]),
        "electronics_pct": pct(totals["electronics"])
    }