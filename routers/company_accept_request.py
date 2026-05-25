
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

@router.patch("/{request_id}/assign")
def accept_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_company_id = Depends(get_curr_company_id)
): 
    """
    Company accepts a pickup request
    - Updates Recyclable_Item status from 'pending' to 'assigned'
    - Creates a new Request record linking company to recyclable_item
    """
    recyclable = db.query(Recyclable_Item).filter(
        Recyclable_Item.id == request_id,
        Recyclable_Item.status.in_(['pending', 'scheduled'])
    ).first()
    
    if not recyclable:
        raise HTTPException(status_code=404, detail="Request not found or already assigned")

    company = db.query(Company).filter(Company.id == current_company_id).first()
    if not company:
        raise HTTPException(status_code=403, detail="Only companies can accept requests")
    
    try:
        recyclable.status = 'assigned'
        recyclable.company_id = company.id
        new_request = Request(
            company_id=company.id,
            recyclable_item_id=request_id  
        )
        
        db.add(new_request)
        db.commit()
        
        return {
            "status": "success",
            "message": "Request accepted successfully",
            "request_id": request_id,
            "company_id": company.id
        }
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to accept request: {str(e)}")
 
 