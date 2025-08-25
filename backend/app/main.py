from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routes.boats import router as boats_router
from app.routes.trips import router as trips_router
from app.routes.tides import router as tides_router
from app.routes.debug import router as debug_router
from app.models import Company, Port  # ensure metadata registers all models



app = FastAPI(title="Boat Schedule API")

# CORS: web + mobile (tune this for your domains)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # dev only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Auto-create tables on first run (later: Alembic)
Base.metadata.create_all(bind=engine)

# Routers
app.include_router(boats_router)
app.include_router(trips_router)
app.include_router(tides_router)
app.include_router(debug_router)
@app.get("/health")
def health():
    return {"ok": True}
