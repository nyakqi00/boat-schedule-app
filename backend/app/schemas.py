from pydantic import BaseModel
from typing import Optional
from datetime import date

class BoatCreate(BaseModel):
    company_id: int
    name: str
    reg_no: str
    license_no: Optional[str] = None
    license_expiry: Optional[date] = None

class BoatOut(BaseModel):
    id: int
    company_id: int
    name: str
    reg_no: str
    license_no: Optional[str] = None
    license_expiry: Optional[date] = None
    class Config:
        from_attributes = True
