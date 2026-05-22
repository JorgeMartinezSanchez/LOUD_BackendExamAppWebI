from typing import Optional, Dict, Any
from uuid import UUID
from fastapi import Depends
from sqlalchemy.orm import Session
from core.database import get_db
from repositories.interfaces import IEventRepository, ITicketTypeRepository
from repositories.event_repository import EventRepository
from repositories.ticket_type_repository import TicketTypeRepository

class EventService:
    """
    Depende de abstracciones (IEventRepository, ITicketTypeRepository),
    no de implementaciones concretas.
    """
    
    def __init__(
        self,
        event_repo: IEventRepository,
        ticket_type_repo: ITicketTypeRepository
    ):
        self.event_repo = event_repo
        self.ticket_type_repo = ticket_type_repo
    
    def list_events(self, q: Optional[str], sort: str, page: int, page_size: int) -> Dict[str, Any]:
        filters = {'q': q, 'sort': sort}
        offset = (page - 1) * page_size
        
        events = self.event_repo.list(filters, page_size, offset)
        total = self.event_repo.count(filters)
        
        return {
            'count': total,
            'page': page,
            'results': self._serialize_events(events)
        }
    
    def get_event_detail(self, event_id: UUID):
        event = self.event_repo.get_by_id(event_id)
        if not event:
            return None
        
        ticket_types = self.ticket_type_repo.list({'event_id': event_id}, 100, 0)
        
        return {
            'id': event.id,
            'title': event.title,
            'tiers': self._serialize_ticket_types(ticket_types)
        }
    
    def _serialize_events(self, events):
        # Lógica de serialización
        pass
    
    def _serialize_ticket_types(self, ticket_types):
        # Lógica de serialización
        pass

# Factory para inyección de dependencias
def get_event_service(db: Session = Depends(get_db)) -> EventService:
    return EventService(
        event_repo=EventRepository(db),      # Inyectamos implementación concreta
        ticket_type_repo=TicketTypeRepository(db)  # pero el servicio depende de la interfaz
    )