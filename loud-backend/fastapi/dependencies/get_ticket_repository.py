from repositories.ticket_type_repository import TicketTypeRepository

_ticket_type_repository: TicketTypeRepository = None

def get_ticket_type_repository() -> TicketTypeRepository:
    """Dependencia de FastAPI para el repositorio de ticket types"""
    global _ticket_type_repository
    if _ticket_type_repository is None:
        _ticket_type_repository = TicketTypeRepository()
    return _ticket_type_repository