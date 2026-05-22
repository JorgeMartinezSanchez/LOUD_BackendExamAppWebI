from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
import os

def get_database_url():
    """Construye la URL de la base de datos con valores seguros"""
    user = os.getenv('POSTGRES_USER', 'postgres')
    password = os.getenv('POSTGRES_PASSWORD', 'postgres')
    host = os.getenv('POSTGRES_HOST', 'postgresql')
    port = os.getenv('POSTGRES_PORT', '5432')
    db = os.getenv('POSTGRES_DB', 'postgres')
    
    # Si el puerto es None o vacío, usar el default
    if not port:
        port = '5432'
    
    return f"postgresql://{user}:{password}@{host}:{port}/{db}"

DATABASE_URL = get_database_url()
print(f"Database URL: postgresql://{os.getenv('POSTGRES_USER', 'postgres')}:****@{os.getenv('POSTGRES_HOST', 'postgresql')}:{os.getenv('POSTGRES_PORT', '5432')}/{os.getenv('POSTGRES_DB', 'postgres')}")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()