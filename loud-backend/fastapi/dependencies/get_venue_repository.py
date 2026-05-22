from repositories.venue_repository import VenueRepository

_venue_repository: VenueRepository = None

def get_venue_repository() -> VenueRepository:
    """Dependencia de FastAPI para el repositorio de venues"""
    global _venue_repository
    if _venue_repository is None:
        _venue_repository = VenueRepository()
    return _venue_repository