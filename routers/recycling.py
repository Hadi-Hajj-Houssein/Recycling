from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db_main import SessionLocal
from functionalities.auth import get_curr_user_id
from models.user_total_recycled import UserTotalRecycled

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
    rec = db.query(UserTotalRecycled).filter(UserTotalRecycled.user_id == user_id).first()

    if not rec:
        return {
            "plastic_pct": 0.0,
            "paper_pct": 0.0,
            "glass_pct": 0.0,
            "metal_pct": 0.0,
            "organic_pct": 0.0,
            "electronics_pct": 0.0
        }

    total = (
        rec.total_plastic +rec.total_paper +rec.total_glass +rec.total_metal +rec.total_organic
    )

    return {
        "plastic_pct": calc_pct(rec.total_plastic, total),
        "paper_pct": calc_pct(rec.total_paper, total),
        "glass_pct": calc_pct(rec.total_glass, total),
        "metal_pct": calc_pct(rec.total_metal, total),
        "organic_pct": calc_pct(rec.total_organic, total),
        "electronics_pct": 0.0
    }