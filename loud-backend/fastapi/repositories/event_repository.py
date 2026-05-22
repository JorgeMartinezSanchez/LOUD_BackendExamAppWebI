from typing import Dict, Any, List, Optional
from uuid import UUID
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from models.event import Event 
from models.ticket_type import TicketType
from base_repository import BaseRepository
from repositories.interfaces import IEventRepository

class EventRepository(BaseRepository[Event], IEventRepository):
    """Cumple SRP: solo responsabilidad de acceso a datos de Event"""
    
    def __init__(self, db: Session):
        super().__init__(db, Event)
    
    # Override para agregar joinedload con venue
    def get_by_id(self, id: UUID) -> Optional[Event]:
        return self.db.query(Event).options(
            joinedload(Event.venue)
        ).filter(Event.id == id).first()
    
    # Override de hooks (Open/Closed - no modificar método list, solo extender)
    def _apply_filters(self, query, filters: Dict[str, Any]):
        if filters.get('q'):
            query = query.filter(Event.title.ilike(f"%{filters['q']}%"))
        
        if filters.get('venue_id'):
            query = query.filter(Event.venue_id == filters['venue_id'])
        
        if filters.get('upcoming'):
            query = query.filter(Event.starts_at > func.now())
        
        return query
    
    def _apply_ordering(self, query, sort: str):
        order_map = {
            'date': Event.starts_at.asc(),
            'price': Event.min_price.asc(),
            'capacity': Event.available.asc(),
        }
        order_by = order_map.get(sort, Event.starts_at.asc())
        return query.order_by(order_by)
    
    # Métodos específicos de la interfaz IEventRepository
    def get_upcoming(self, limit: int = 10) -> List[Event]:
        return self.db.query(Event).filter(
            Event.starts_at > func.now()
        ).order_by(Event.starts_at.asc()).limit(limit).all()
    
    def search_by_title(self, query: str, limit: int, offset: int) -> List[Event]:
        return self.db.query(Event).filter(
            Event.title.ilike(f"%{query}%")
        ).offset(offset).limit(limit).all()
    
    def update_availability_from_tiers(self, event_id: UUID) -> None:
        total_available = self.db.query(
            func.coalesce(func.sum(TicketType.available), 0)
        ).filter(TicketType.event_id == event_id).scalar() or 0
        
        self.db.query(Event).filter(Event.id == event_id).update(
            {'available': total_available}
        )
        self.db.commit()