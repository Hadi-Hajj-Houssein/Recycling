from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from db_main import get_db
from models.Recyclables import Recyclable_Item
from functionalities.auth import get_curr_user_id
from models.user_total_recycled import UserTotalRecycled
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
router = APIRouter(prefix="/recyclables", tags=["recyclables"])
class ItemIn(BaseModel):
    """Shape of data the frontend sends (POST / PUT body)."""
    type:      str
    name:      str
    desc:      Optional[str] = ""
    weight:    float
    condition: str = "clean"
    status:    str = "pending"
    date:      Optional[datetime] = None
    company_id : Optional[int] = None


class ItemOut(BaseModel):
    """Shape of data returned to the frontend."""
    id:        int
    user_id:   int
    type:      str
    name:      str
    desc:      Optional[str] = ""
    weight:    float
    condition: str
    status:    str
    date:      datetime
    company_id: Optional[int] = None 

    class Config:
        from_attributes = True   
VALID_TYPES      = {"plastic", "paper", "glass", "metal", "electronics", "organic"}
VALID_CONDITIONS = {"clean", "slightly_dirty", "dirty"}
VALID_STATUSES   = {"pending", "scheduled", "collected"}


def _validate(data: ItemIn):
    if data.type not in VALID_TYPES:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
                            f"type must be one of: {VALID_TYPES}")
    if data.condition not in VALID_CONDITIONS:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
                            f"condition must be one of: {VALID_CONDITIONS}")
    if data.status not in VALID_STATUSES:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
                            f"status must be one of: {VALID_STATUSES}")



class RecyclableUpdate(BaseModel):
    status:         Optional[str]      = None
    scheduled_date: Optional[datetime] = None
    company_id:     Optional[int]      = None
    name:           Optional[str]      = None
    type:           Optional[str]      = None
    weight:         Optional[float]    = None
    condition:      Optional[str]      = None
    desc:           Optional[str]      = None


def _sync_summary(db: Session, user_id: int):
    rows = db.query(Recyclable_Item).filter(
        Recyclable_Item.user_id == user_id,
        Recyclable_Item.status == "collected"
    ).all()

    totals = {
        "organic": 0.0,
        "paper": 0.0,
        "plastic": 0.0,
        "glass": 0.0,
        "metal": 0.0
    }

    for r in rows:
        if r.type in totals:
            totals[r.type] += r.weight

    summary = db.query(UserTotalRecycled).filter(
        UserTotalRecycled.user_id == user_id
    ).first()

    if summary is None:
        summary = UserTotalRecycled(
            user_id=user_id,
            total_organic=totals["organic"],
            total_paper=totals["paper"],
            total_plastic=totals["plastic"],
            total_glass=totals["glass"],
            total_metal=totals["metal"],
        )
        db.add(summary)
    else:
        summary.total_organic = totals["organic"]
        summary.total_paper = totals["paper"]
        summary.total_plastic = totals["plastic"]
        summary.total_glass = totals["glass"]
        summary.total_metal = totals["metal"]

    db.commit()
@router.get("", response_model=List[ItemOut])
def get_items(
    db:           Session = Depends(get_db),
    current_user: int     = Depends(get_curr_user_id),
):
    return (
        db.query(Recyclable_Item)
          .filter(Recyclable_Item.user_id == current_user)
          .order_by(Recyclable_Item.date.desc())
          .all()
    )


@router.post("", response_model=ItemOut, status_code=status.HTTP_201_CREATED)
def create_item(
    payload:      ItemIn,
    db:           Session = Depends(get_db),
    current_user: int     = Depends(get_curr_user_id),
):
    _validate(payload)

    item = Recyclable_Item(
        user_id   = current_user,
        type      = payload.type,
        name      = payload.name,
        desc      = payload.desc or "",
        weight    = payload.weight,
        condition = payload.condition,
        status    = payload.status,
        date      = payload.date or datetime.utcnow(),
        company_id = payload.company_id,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    _sync_summary(db, current_user)
    return item


@router.put("/{item_id}", response_model=ItemOut)
def update_item(
    item_id:      int,
    payload:      ItemIn,
    db:           Session = Depends(get_db),
    current_user: int     = Depends(get_curr_user_id),
):
    item = db.query(Recyclable_Item).filter(
        Recyclable_Item.id      == item_id,
        Recyclable_Item.user_id == current_user,
    ).first()

    if not item:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Item not found")

    _validate(payload)
    item.type      = payload.type
    item.name      = payload.name
    item.desc      = payload.desc or ""
    item.weight    = payload.weight
    item.condition = payload.condition
    item.status    = payload.status
    item.company_id = payload.company_id  

    db.commit()
    db.refresh(item)
    _sync_summary(db, current_user)
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(
    item_id:      int,
    db:           Session = Depends(get_db),
    current_user: int     = Depends(get_curr_user_id),
):
    item = db.query(Recyclable_Item).filter(
        Recyclable_Item.id      == item_id,
        Recyclable_Item.user_id == current_user,
    ).first()

    if not item:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Item not found")

    db.delete(item)
    db.commit()
    _sync_summary(db, current_user)

    
@router.put("/recyclables/{item_id}")
def update_recyclable(
    item_id: int,
    body: RecyclableUpdate,
    user_id: int = Depends(get_curr_user_id),
    db: Session = Depends(get_db)
):
    item = db.query(Recyclable_Item).filter(
        Recyclable_Item.id == item_id,
        Recyclable_Item.user_id == user_id
    ).first()

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    if body.status is not None:
        allowed = {"pending", "scheduled", "collected"}
        if body.status not in allowed:
            raise HTTPException(status_code=400, detail=f"status must be one of {allowed}")
        item.status = body.status

    if body.scheduled_date is not None:
        item.scheduled_date = body.scheduled_date

    if body.company_id  is not None: item.company_id  = body.company_id
    if body.name        is not None: item.name        = body.name
    if body.type        is not None: item.type        = body.type
    if body.weight      is not None: item.weight      = body.weight
    if body.condition   is not None: item.condition   = body.condition
    if body.desc        is not None: item.desc        = body.desc

    db.commit()
    db.refresh(item)

    return {
        "id":             item.id,
        "user_id":        item.user_id,
        "company_id":     item.company_id,
        "company_name":   item.company_name if item.company else None,
        "type":           item.type,
        "name":           item.name,
        "desc":           item.desc,
        "weight":         item.weight,
        "condition":      item.condition,
        "status":         item.status,
        "date":           item.date,
        "scheduled_date": item.scheduled_date,
    }