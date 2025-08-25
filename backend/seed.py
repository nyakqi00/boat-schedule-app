from datetime import datetime, timedelta
from app.database import Base, engine, SessionLocal
from app.models import Company, Port, Boat, Trip, TripStatus

# Reset database (drop + create tables)
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# --------------------------
# Companies
# --------------------------
c1 = Company(name="East Coast Fisheries")
c2 = Company(name="South Sea Ventures")
db.add_all([c1, c2])
db.commit()

# --------------------------
# Ports
# --------------------------
p1 = Port(
    name="Kuantan Port",
    location="Kuantan, Malaysia",
    mean_low_water_depth_m=3.5,
    timezone="Asia/Kuala_Lumpur"
)
p2 = Port(
    name="Kuala Terengganu Port",
    location="Kuala Terengganu, Malaysia",
    mean_low_water_depth_m=4.0,
    timezone="Asia/Kuala_Lumpur"
)
db.add_all([p1, p2])
db.commit()

# --------------------------
# Boats
# --------------------------
b1 = Boat(company_id=c1.id, reg_no="ECF-001", name="Blue Marlin", length_m=20.5, draft_m=2.2)
b2 = Boat(company_id=c1.id, reg_no="ECF-002", name="Golden Tuna", length_m=18.0, draft_m=2.0)
b3 = Boat(company_id=c2.id, reg_no="SSV-001", name="Sea Voyager", length_m=22.0, draft_m=2.5)
db.add_all([b1, b2, b3])
db.commit()

# --------------------------
# Trips
# --------------------------
t1 = Trip(
    company_id=c1.id,
    boat_id=b1.id,
    port_out_id=p1.id,
    departed_at=datetime.utcnow() - timedelta(days=5),
    est_return_at=datetime.utcnow() + timedelta(days=5),
    status=TripStatus.at_sea,
    notes="Routine fishing trip."
)
t2 = Trip(
    company_id=c1.id,
    boat_id=b2.id,
    port_out_id=p1.id,
    departed_at=datetime.utcnow() - timedelta(days=15),
    est_return_at=datetime.utcnow() - timedelta(days=5),
    port_in_id=p2.id,
    arrived_at=datetime.utcnow() - timedelta(days=4),
    status=TripStatus.arrived,
    notes="Brought in large tuna catch."
)
t3 = Trip(
    company_id=c2.id,
    boat_id=b3.id,
    port_out_id=p2.id,
    departed_at=datetime.utcnow() - timedelta(days=2),
    est_return_at=datetime.utcnow() + timedelta(days=8),
    status=TripStatus.planned,
    notes="Heading towards South China Sea."
)
db.add_all([t1, t2, t3])
db.commit()

db.close()
print("✅ Seed data inserted successfully!")
