
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
from models.company import Company
from models.requests import Request
router = APIRouter()
@router.patch("/{request_id}/decline")
def decline_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_company_id = Depends(get_curr_company_id)
):
    recyclable = db.query(Recyclable_Item).filter(
        Recyclable_Item.id == request_id,
        Recyclable_Item.status.in_(['pending', 'scheduled'])
    ).first()

    if not recyclable:
        raise HTTPException(status_code=404, detail="Request not found or not in pending state")

    company = db.query(Company).filter(Company.id == current_company_id).first()
    if not company:
        raise HTTPException(status_code=403, detail="Only companies can decline requests")

    try:
        recyclable.status = 'pending'  
        recyclable.company_id = None
        db.commit()               

        return {
            "status": "success",
            "message": "Request declined successfully",
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to decline request: {str(e)}")