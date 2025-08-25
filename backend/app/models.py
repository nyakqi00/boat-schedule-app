from sqlalchemy import (
    Column, Integer, String, Float, Boolean,
    DateTime, Enum, ForeignKey, UniqueConstraint
)
from sqlalchemy.orm import relationship
import enum

from app.database import Base

class TripStatus(str, enum.Enum):
    planned = "planned"
    at_sea = "at_sea"
    arrived = "arrived"
    delayed = "delayed"
    cancelled = "cancelled"

class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True)
    name = Column(String(120), unique=True, nullable=False)

class Boat(Base):
    __tablename__ = "boats"
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False)
    reg_no = Column(String(64), nullable=False)
    name = Column(String(120), nullable=False)
    length_m = Column(Float, default=0)
    draft_m = Column(Float, default=1.2)
    is_active = Column(Boolean, default=True, nullable=False)

    company = relationship("Company", lazy="joined")

    __table_args__ = (UniqueConstraint("company_id", "reg_no", name="uq_company_reg"),)

class Port(Base):
    __tablename__ = "ports"
    id = Column(Integer, primary_key=True)
    name = Column(String(120), unique=True, nullable=False)
    location = Column(String(255))  # 👈 NEW
    mean_low_water_depth_m = Column(Float, default=2.0)
    timezone = Column(String(64), default="Asia/Kuala_Lumpur")

class Tide(Base):
    __tablename__ = "tides"
    id = Column(Integer, primary_key=True)
    port_id = Column(Integer, ForeignKey("ports.id", ondelete="CASCADE"), nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False)
    water_level_m = Column(Float, nullable=False)  # above chart datum

    port = relationship("Port")

class Trip(Base):
    __tablename__ = "trips"
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False)
    boat_id = Column(Integer, ForeignKey("boats.id", ondelete="CASCADE"), nullable=False)
    port_out_id = Column(Integer, ForeignKey("ports.id"), nullable=False)
    departed_at = Column(DateTime(timezone=True), nullable=False)
    est_return_at = Column(DateTime(timezone=True), nullable=False)
    port_in_id = Column(Integer, ForeignKey("ports.id"), nullable=True)
    arrived_at = Column(DateTime(timezone=True), nullable=True)
    status = Column(Enum(TripStatus), default=TripStatus.at_sea, nullable=False)
    notes = Column(String(500))

    company = relationship("Company")
    boat = relationship("Boat")
    port_out = relationship("Port", foreign_keys=[port_out_id])
    port_in = relationship("Port", foreign_keys=[port_in_id])
