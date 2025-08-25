from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Trip, Boat, TripStatus
from app.schemas import TripCreate, TripOut, ArriveIn

router = APIRouter(prefix="/trips", tags=["trips"])

def estimate_return(departed_at: datetime, est_days: int) -> datetime:
    return departed_at + timedelta(days=est_days)

@router.post("", response_model=TripOut)
def create_trip(payload: TripCreate, db: Session = Depends(get_db)):
    boat = db.get(Boat, payload.boat_id)
    if not boat or boat.company_id != payload.company_id:
        raise HTTPException(400, "Boat not found or not in company")

    trip = Trip(
        company_id=payload.company_id,
        boat_id=payload.boat_id,
        port_out_id=payload.port_out_id,
        departed_at=payload.departed_at,
        est_return_at=estimate_return(payload.departed_at, payload.est_days),
        status=TripStatus.at_sea,
    )
    db.add(trip)
    db.commit()
    db.refresh(trip)
    return trip

@router.get("", response_model=list[TripOut])
def list_trips(company_id: int, status: str | None = None, db: Session = Depends(get_db)):
    q = db.query(Trip).filter(Trip.company_id == company_id)
    if status:
        q = q.filter(Trip.status == TripStatus(status))
    return q.order_by(Trip.departed_at.desc()).all()

@router.patch("/{trip_id}/arrive", response_model=TripOut)
def arrive(trip_id: int, payload: ArriveIn, db: Session = Depends(get_db)):
    trip = db.get(Trip, trip_id)
    if not trip:
        raise HTTPException(404, "Trip not found")
    trip.port_in_id = payload.port_in_id
    trip.arrived_at = payload.arrived_at or datetime.utcnow()
    trip.status = TripStatus.arrived
    if payload.notes:
        trip.notes = payload.notes
    db.commit()
    db.refresh(trip)
    return trip
