from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+psycopg://postgres:postgres@localhost:5432/boats"
    APP_TZ: str = "Asia/Kuala_Lumpur"
    DEFAULT_TRIP_DAYS: int = 10
    SAFETY_MARGIN_M: float = 0.5

settings = Settings()
