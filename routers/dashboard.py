from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from db_main import get_db
from functionalities.auth import get_curr_user_id
from models.user_total_recycled import UserTotalRecycled

router = APIRouter()
templates = Jinja2Templates(directory="frontend")# bet oul la fastapi anno elmfrontend bel folder frontend
@router.get("/dashboard") # bta3mol run lamma el user ykoun bel / dashboard
def dashboard(
    request: Request,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_curr_user_id),
):
    
    totals= db.query(UserTotalRecycled).filter(UserTotalRecycled.user_id == current_user).first()
    organic = totals.total_organic if totals else 0
    paper = totals.total_paper if totals else 0
    plastic = totals.total_plastic if totals else 0
    glass = totals.total_glass if totals else 0
    metal = totals.total_metal if totals else 0
    electronics = 0#totals.total_electronics if totals else 0
    total = organic + paper + plastic + glass + metal + electronics
    if(total>0):
        organic_pct = round((organic/total)*100,1)
        paper_pct = round((paper/total)*100,1)
        plastic_pct =round((plastic/total)*100,1)
        glass_pct =round((glass/total)*100,1)
        metal_pct =round((metal/total)*100,1)
        electronics_pct = 0#round((electronics/total)*100,1)

    else:
        organic_pct = 0
        paper_pct = 0
        plastic_pct = 0
        glass_pct = 0
        metal_pct = 0
        electronics_pct = 0

    return templates.TemplateResponse("/dashboard", {
        "request": request,
        "total": total,
        "organic": organic,
        "paper": paper,
        "plastic": plastic,
        "glass": glass,
        "metal": metal,
        "electronics": electronics,
        "organic_pct": organic_pct,
        "paper_pct": paper_pct,
        "plastic_pct": plastic_pct,
        "glass_pct": glass_pct,
        "metal_pct": metal_pct,
        "electronics_pct": electronics_pct
    })
