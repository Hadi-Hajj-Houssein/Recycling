
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timezone
from collections import defaultdict
from sqlalchemy import desc
from sqlalchemy.orm import Session
from db_main import SessionLocal
from functionalities.auth import get_curr_user_id , get_curr_company_id
from models.Recyclables import Recyclable_Item
from routers.dependencies import get_db

router = APIRouter()

@router.get("/company/user_requests")
def get_user_requests(
    company_id: int = Depends(get_curr_company_id),
    db: Session = Depends(get_db)
):
    items = db.query(Recyclable_Item).filter(
        Recyclable_Item.company_id == company_id
    ).all()
    return [
        {
            "id":         r.id,
            "user_id":    r.user_id,
            "type":       r.type,
            "name":       r.name,
            "desc":       r.desc,
            "weight":     r.weight,
            "condition":  r.condition,
            "status":     r.status,
            "date": r.date.isoformat() if r.date else None, 
            "address":    getattr(r, 'address', 'No address yet'),
            "area":       getattr(r, 'area', 'Unknown'),
            "phone":      getattr(r, 'phone', None),
        }
        for r in items
    ]