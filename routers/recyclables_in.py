from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

from db_main import get_db
from models.Recyclables import Recyclable_Item
from functionalities.auth import get_curr_user_id

router = APIRouter(prefix="/recyclables", tags=["recyclables"])


# ── Pydantic Schemas ───────────────────────────────────────────────────────────

class ItemIn(BaseModel):
    """Shape of data the frontend sends (POST / PUT body)."""
    type:      str
    name:      str
    desc:      Optional[str] = ""
    weight:    float
    condition: str = "clean"
    status:    str = "pending"
    date:      Optional[datetime] = None


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

    class Config:
        from_attributes = True   # Pydantic v2 — use orm_mode=True if on v1


# ── Validation ─────────────────────────────────────────────────────────────────

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


# ── Summary sync ───────────────────────────────────────────────────────────────

def _sync_summary(db: Session, user_id: int):
    """Recalculate and upsert the Recyclables summary row for this user."""
    try:
        from models import Recyclables
        rows   = db.query(Recyclable_Item).filter(Recyclable_Item.user_id == user_id).all()
        totals = {t: 0.0 for t in ("plastic", "paper", "glass", "metal", "organic")}
        for r in rows:
            if r.type in totals:
                totals[r.type] += r.weight
        summary = db.query(Recyclables).filter(Recyclables.user_id == user_id).first()
        if summary is None:
            summary = Recyclables(user_id=user_id, **totals)
            db.add(summary)
        else:
            for k, v in totals.items():
                setattr(summary, k, v)
        db.commit()
    except Exception:
        pass


# ── Endpoints ──────────────────────────────────────────────────────────────────

@router.get("", response_model=List[ItemOut])
def get_items(
    db:           Session = Depends(get_db),
    current_user: int     = Depends(get_curr_user_id),
):
    """Return all recyclable items for the authenticated user."""
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
    """Log a new recyclable item for the authenticated user."""
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
    """Update an item. Returns 404 if it doesn't belong to the current user."""
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
    """Delete an item. Returns 404 if it doesn't belong to the current user."""
    item = db.query(Recyclable_Item).filter(
        Recyclable_Item.id      == item_id,
        Recyclable_Item.user_id == current_user,
    ).first()

    if not item:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Item not found")

    db.delete(item)
    db.commit()
    _sync_summary(db, current_user)