from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models import Tide, Port, Boat
from app.schemas import TideCreate, TideOut, TideCheckIn, TideCheckOut

router = APIRouter(prefix="/tides", tags=["tides"])

@router.post("", response_model=TideOut)
def create_tide(payload: TideCreate, db: Session = Depends(get_db)):
    t = Tide(**payload.model_dump())
    db.add(t)
    db.commit()
    db.refresh(t)
    return t

@router.get("", response_model=list[TideOut])
def list_tides(port_id: int, db: Session = Depends(get_db)):
    q = db.query(Tide).filter(Tide.port_id == port_id)
    return q.order_by(Tide.timestamp.asc()).all()

@router.post("/check", response_model=TideCheckOut)
def tide_check(payload: TideCheckIn, db: Session = Depends(get_db)):
    # figure out draft
    draft = payload.boat_draft_m
    if draft is None and payload.boat_id:
        boat = db.get(Boat, payload.boat_id)
        draft = boat.draft_m if boat else None

    required = (draft + payload.safety_margin_m) if draft is not None else None

    # nearest tide reading to arrival_time
    nearest = (
        db.query(Tide)
        .filter(Tide.port_id == payload.port_id)
        .order_by(func.abs(func.extract('epoch', Tide.timestamp - payload.arrival_time)))
        .first()
    )

    if not nearest or required is None:
        return TideCheckOut(
            can_enter=False,
            water_level_m=(nearest.water_level_m if nearest else None),
            required_level_m=required,
            nearest_reading_time=(nearest.timestamp if nearest else None),
        )

    can = nearest.water_level_m >= required
    return TideCheckOut(
        can_enter=can,
        water_level_m=nearest.water_level_m,
        required_level_m=required,
        nearest_reading_time=nearest.timestamp,
    )
