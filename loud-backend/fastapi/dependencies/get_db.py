from sqlalchemy.orm import Session
from core.database import SessionLocal

def get_db() -> Session: # type: ignore
    """Dependencia de FastAPI para obtener sesión de BD"""
    db = SessionLocal()
    try:
        yield db  # type: ignore
    finally:
        db.close()