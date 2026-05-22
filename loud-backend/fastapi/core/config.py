import os

# CAMBIAR LAS VARIABLES NO OLVIDAR

class Settings:
    POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'postgresql')
    POSTGRES_DB = os.getenv('POSTGRES_DB', 'postgres')
    POSTGRES_USER = os.getenv('POSTGRES_USER', 'postgres')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'postgres')
    POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')
    
    REDIS_HOST = os.getenv('REDIS_HOST', 'redis')
    REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
    
    CACHE_TTL = int(os.getenv('CACHE_TTL', 60))  # segundos

settings = Settings()