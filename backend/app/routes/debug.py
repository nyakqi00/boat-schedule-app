from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Company, Boat, Trip, Port

router = APIRouter(prefix="/debug", tags=["debug"])

@router.get("/companies")
def get_companies(db: Session = Depends(get_db)):
    return db.query(Company).all()

@router.get("/boats")
def get_boats(db: Session = Depends(get_db)):
    return db.query(Boat).all()

@router.get("/ports")
def get_ports(db: Session = Depends(get_db)):
    return db.query(Port).all()

@router.get("/trips")
def get_trips(db: Session = Depends(get_db)):
    return db.query(Trip).all()
