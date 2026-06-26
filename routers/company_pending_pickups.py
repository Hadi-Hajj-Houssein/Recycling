from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from routers.dependencies import get_db
from functionalities.auth import get_curr_company_id
from models.Recyclables import Recyclable_Item

router = APIRouter()
@router.get("/company/pending-pickups")
def get_pending_pickups(
    db:Session= Depends(get_db),
    current_company_id = Depends(get_curr_company_id)
):
    items = db.query(Recyclable_Item).filter(
        Recyclable_Item.company_id == current_company_id,
        Recyclable_Item.status == 'assigned'
    ).all()
    return [
        {
            "id":             item.id,
            "name":           item.user.username,
            "phone":          item.user.phone_number,
            "address":        "soon",   # check User model has this
            "materials":      [item.type],            #  7a tsir list la hek soon 
            "weight":         item.weight,
            "scheduled_date": item.scheduled_date.isoformat() if item.scheduled_date else None,
            "status":         item.status,
        }
        for item in items
    ]