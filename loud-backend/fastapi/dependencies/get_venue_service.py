from fastapi import Depends
from services.venue_service import VenueService
from dependencies.get_venue_repository import get_venue_repository
from dependencies.get_cache import get_cache
from repositories.venue_repository import VenueRepository
from cache.base import Cache

def get_venue_service(
    repository: VenueRepository = Depends(get_venue_repository),
    cache: Cache = Depends(get_cache)
) -> VenueService:
    """Dependencia de FastAPI para el servicio de venues"""
    return VenueService(repository, cache)