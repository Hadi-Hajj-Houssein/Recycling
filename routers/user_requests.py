from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# Your database connection
from db_main import SessionLocal

# Your models (adjust path if needed)
from models.Recyclables import Recyclable_Item
from models.user import User

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/api/requests")
def get_all_requests(db: Session = Depends(get_db)):
    query_results = db.query(Recyclable_Item, User).join(User, Recyclable_Item.user_id == User.id).all()
    
    formatted_data = []
    for item, user in query_results:
        formatted_data.append({
            "id": f"{item.id}",
            "name": f"{user.first_name} {user.last_name}",
            "initials": f"{user.first_name[0]}{user.last_name[0]}",
            "area": "Lebanon", 
            "address": "Pickup Location", 
            "materials": [item.type.lower()] if item.type else ["unknown"],
            "weight": item.weight or 0,
            "date": item.date, # You can update this to item.date later
            "status": item.status or "new",
            "score": user.amount or 0,
            "phone": "+961-XX-XXXXXX",
            "notes": item.desc or ""
        })
    return formatted_data