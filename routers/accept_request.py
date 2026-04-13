from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db_main import SessionLocal
from models.Recyclables import Recyclable_Item

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.patch("/requests/{request_id}/assign")
def assign_request(request_id: int, db: Session = Depends(get_db)):
    req = db.query(Recyclable_Item).filter(Recyclable_Item.id == request_id).first()

    if not req:
        raise HTTPException(status_code=404, detail="Recyclable_Item not found")

    req.status = "assigned"

    db.commit()
    db.refresh(req)

    return {"message": "Recyclable_Item assigned", "id": req.id}