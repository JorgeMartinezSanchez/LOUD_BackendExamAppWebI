from repositories.event_repository import EventRepository

_event_repository: EventRepository = None

def get_event_repository() -> EventRepository:
    """Dependencia de FastAPI para el repositorio de eventos"""
    global _event_repository
    if _event_repository is None:
        _event_repository = EventRepository()
    return _event_repository