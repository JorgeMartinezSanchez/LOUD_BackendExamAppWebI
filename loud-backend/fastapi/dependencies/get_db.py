from typing import Generator
import psycopg2
from psycopg2.extras import RealDictCursor
from core.config import settings

def get_db_connection():
    """Obtiene una conexión directa a PostgreSQL (no administrada por FastAPI)"""
    return psycopg2.connect(
        host=settings.POSTGRES_HOST,
        database=settings.POSTGRES_DB,
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        port=settings.POSTGRES_PORT,
        cursor_factory=RealDictCursor
    )

def get_db_dependency() -> Generator:
    """Dependencia de FastAPI que provee una conexión y la cierra automáticamente"""
    conn = None
    try:
        conn = get_db_connection()
        yield conn
    finally:
        if conn:
            conn.close()