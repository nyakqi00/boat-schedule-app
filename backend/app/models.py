from sqlalchemy import Column, BigInteger, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Company(Base):
    __tablename__ = "companies"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(120), unique=True, nullable=False)

class Boat(Base):
    __tablename__ = "boats"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    company_id = Column(BigInteger, ForeignKey("companies.id"), nullable=False, index=True)
    name = Column(String(120), nullable=False)
    reg_no = Column(String(80), nullable=False)
    license_no = Column(String(80))
    license_expiry = Column(Date)

    company = relationship("Company")

class Crew(Base):
    __tablename__ = "crew"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    company_id = Column(BigInteger, ForeignKey("companies.id"), nullable=False, index=True)
    boat_id = Column(BigInteger, ForeignKey("boats.id"), index=True, nullable=True)
    name = Column(String(120), nullable=False)
    nationality = Column(String(60))
    passport_no = Column(String(60))
    visa_expiry = Column(Date)
    license_type = Column(String(60))
    license_expiry = Column(Date)

class Trip(Base):
    __tablename__ = "trips"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    company_id = Column(BigInteger, ForeignKey("companies.id"), nullable=False, index=True)
    boat_id = Column(BigInteger, ForeignKey("boats.id"), nullable=False, index=True)
    departure_at = Column(DateTime, nullable=False)
    estimated_return_at = Column(DateTime)
    actual_return_at = Column(DateTime)
    status = Column(String(12), default="AT_SEA")  # AT_SEA | RETURNED | OVERDUE
