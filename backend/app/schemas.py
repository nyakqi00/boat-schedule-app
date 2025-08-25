from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime

class BoatCreate(BaseModel):
    company_id: int
    reg_no: str
    name: str
    length_m: float = 0
    draft_m: float = 1.2

class BoatOut(BaseModel):
    id: int
    company_id: int
    reg_no: str
    name: str
    length_m: float
    draft_m: float
    is_active: bool
    class Config: from_attributes = True

class TripCreate(BaseModel):
    company_id: int
    boat_id: int
    port_out_id: int
    departed_at: datetime
    est_days: int = Field(default=10, ge=8, le=20)

class TripOut(BaseModel):
    id: int
    company_id: int
    boat_id: int
    port_out_id: int
    departed_at: datetime
    est_return_at: datetime
    status: Literal["planned","at_sea","arrived","delayed","cancelled"]
    class Config: from_attributes = True

class ArriveIn(BaseModel):
    port_in_id: int
    arrived_at: Optional[datetime] = None
    notes: Optional[str] = None

class PortCreate(BaseModel):
    name: str
    mean_low_water_depth_m: float = 2.0
    timezone: str = "Asia/Kuala_Lumpur"

class PortOut(BaseModel):
    id: int
    name: str
    mean_low_water_depth_m: float
    timezone: str
    class Config: from_attributes = True

class TideCreate(BaseModel):
    port_id: int
    timestamp: datetime
    water_level_m: float

class TideOut(BaseModel):
    id: int
    port_id: int
    timestamp: datetime
    water_level_m: float
    class Config: from_attributes = True

class TideCheckIn(BaseModel):
    port_id: int
    arrival_time: datetime
    # either pass boat_id OR the raw draft, supporting ad-hoc checks
    boat_id: Optional[int] = None
    boat_draft_m: Optional[float] = None
    safety_margin_m: float = 0.5

class TideCheckOut(BaseModel):
    can_enter: bool
    water_level_m: Optional[float] = None
    required_level_m: Optional[float] = None
    nearest_reading_time: Optional[datetime] = None
