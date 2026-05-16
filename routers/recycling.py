from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timezone
from collections import defaultdict
from sqlalchemy import desc
from sqlalchemy.orm import Session
from db_main import SessionLocal
from functionalities.auth import get_curr_user_id
from models.Recyclables import Recyclable_Item
from routers.dependencies import get_db

router = APIRouter()

def pct(val: float, total: float) -> float:
    if total == 0:
        return 0.0
    return round((val / total) * 100, 1)

def time_ago(dt: datetime) -> str:
    if not dt:
        return ""
    now = datetime.now(timezone.utc)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    diff = int((now - dt).total_seconds())
    if diff < 3600:
        return f"{diff // 60}m ago"
    if diff < 86400:
        return f"{diff // 3600}h ago"
    return f"{diff // 86400}d ago"


@router.get("/dashboard")
def dashboard_data(
    user_id: int = Depends(get_curr_user_id),
    db: Session = Depends(get_db)
):
    items = db.query(Recyclable_Item).filter(
        Recyclable_Item.user_id == user_id
    ).all()

    totals = {"plastic":0.0,"paper":0.0,"glass":0.0,"metal":0.0,"organic":0.0,"electronics":0.0}
    for item in items:
        if item.type in totals:
            totals[item.type] += item.weight
    total_weight = sum(totals.values())

    completed_pickups = sum(1 for i in items if i.status == "collected")

    TYPE_EMOJI = {
        "plastic":"🥤","paper":"📄","glass":"🍶",
        "metal":"🔧","electronics":"💻","organic":"🌿"
    }
    STATUS_ICON  = {"collected":"pickup","scheduled":"pickup","pending":"recycle"}
    STATUS_LABEL = {"collected":"Pickup Completed","scheduled":"Pickup Scheduled","pending":"Items Logged"}

    recent = sorted(items, key=lambda x: x.date or datetime.min, reverse=True)[:10]
    activity = []
    for item in recent:
        company_name = item.company.company_name if item.company else None
        desc_text = (
            f"{item.weight}kg {item.type} — {company_name}"
            if company_name else
            f"{item.weight}kg {item.type} logged"
        )
        activity.append({
            "icon_type":   STATUS_ICON.get(item.status, "recycle"),
            "title":       STATUS_LABEL.get(item.status, "Item Updated"),
            "description": desc_text,
            "time_ago":    time_ago(item.date),
            "emoji":       TYPE_EMOJI.get(item.type, "♻️"),
        })

    now_utc = datetime.now(timezone.utc)
    upcoming = [
        i for i in items
        if i.status == "scheduled"
        and i.scheduled_date is not None
        and (
            i.scheduled_date.replace(tzinfo=timezone.utc)
            if i.scheduled_date.tzinfo is None
            else i.scheduled_date
        ) >= now_utc
    ]
    upcoming.sort(key=lambda x: x.scheduled_date)

    next_pickup = None
    if upcoming:
        first = upcoming[0]
        sd = first.scheduled_date
        same_slot = [
            i for i in upcoming
            if i.company_id == first.company_id
            and i.scheduled_date.date() == sd.date()
        ]
        by_type = defaultdict(float)
        for i in same_slot:
            by_type[i.type] += i.weight
        tags = [
            f"{TYPE_EMOJI.get(t,'♻️')} {t.capitalize()} {w:.1f}kg"
            for t, w in by_type.items()
        ]
        next_pickup = {
            "company":    first.company.company_name if first.company else "Unknown",
            "date_day":   sd.strftime("%d"),
            "date_month": sd.strftime("%b"),
            "time_range": sd.strftime("%I:%M %p"),
            "tags":       tags,
        }

    MONTHLY_TARGET = 50.0
    month_weight = sum(
        i.weight for i in items
        if i.status == "collected"
        and i.date
        and (i.date.replace(tzinfo=timezone.utc) if i.date.tzinfo is None else i.date).month == now_utc.month
        and (i.date.replace(tzinfo=timezone.utc) if i.date.tzinfo is None else i.date).year  == now_utc.year
    )
    monthly_goal_pct = min(round((month_weight / MONTHLY_TARGET) * 100, 1), 100)

    return {
        "plastic_pct":      pct(totals["plastic"],      total_weight),
        "paper_pct":        pct(totals["paper"],        total_weight),
        "glass_pct":        pct(totals["glass"],        total_weight),
        "metal_pct":        pct(totals["metal"],        total_weight),
        "organic_pct":      pct(totals["organic"],      total_weight),
        "electronics_pct":  pct(totals["electronics"],  total_weight),
        "total_recycled":   round(total_weight, 2),
        "completed_pickups": completed_pickups,
        "activity":          activity,
        "next_pickup":       next_pickup,
        "monthly_goal_pct":  monthly_goal_pct,
    }


