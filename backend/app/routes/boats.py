from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..models import Boat
from ..schemas import BoatCreate, BoatOut

router = APIRouter(prefix="/boats", tags=["boats"])

async def get_company_id(x_company_id: Optional[int] = Header(None)):
    if not x_company_id:
        raise HTTPException(400, "X-Company-Id header required")
    return x_company_id

@router.get("", response_model=List[BoatOut])
def list_boats(db: Session = Depends(get_db), company_id: int = Depends(get_company_id)):
    return db.query(Boat).filter(Boat.company_id == company_id).order_by(Boat.id).all()

@router.post("", response_model=BoatOut)
def create_boat(payload: BoatCreate, db: Session = Depends(get_db), company_id: int = Depends(get_company_id)):
    if payload.company_id != company_id:
        raise HTTPException(403, "company_id mismatch")
    b = Boat(**payload.model_dump())
    db.add(b)
    db.commit()
    db.refresh(b)
    return b
