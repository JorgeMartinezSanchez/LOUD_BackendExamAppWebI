from fastapi import Depends
from services.event_service import EventService
from dependencies.get_event_repository import get_event_repository
from dependencies.get_cache import get_cache
from repositories.event_repository import EventRepository
from cache.base import Cache

def get_event_service(
    repository: EventRepository = Depends(get_event_repository),
    cache: Cache = Depends(get_cache)
) -> EventService:
    """Dependencia de FastAPI para el servicio de eventos (inyección de dependencias)"""
    return EventService(repository, cache)