from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Boat
from app.schemas import BoatCreate, BoatOut

router = APIRouter(prefix="/boats", tags=["boats"])

@router.post("", response_model=BoatOut)
def create_boat(payload: BoatCreate, db: Session = Depends(get_db)):
    boat = Boat(**payload.model_dump())
    db.add(boat)
    db.commit()
    db.refresh(boat)
    return boat

@router.get("", response_model=list[BoatOut])
def list_boats(company_id: int, db: Session = Depends(get_db)):
    q = db.query(Boat).filter(Boat.company_id == company_id, Boat.is_active == True)
    return q.order_by(Boat.id.desc()).all()
