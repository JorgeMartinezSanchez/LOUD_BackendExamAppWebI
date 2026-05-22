from typing import Optional, Dict, Any
from uuid import UUID
from sqlalchemy.orm import Session
from models.event import Event
from models.venue import Venue
from models.ticket_type import TicketType

class EventService:
    
    def __init__(self, db: Session):
        self.db = db
    
    def list_events(self, q: Optional[str], sort: str, page: int, page_size: int) -> Dict[str, Any]:
        query = self.db.query(Event).join(Venue, Event.venue_id == Venue.id)
        
        if q:
            query = query.filter(Event.title.ilike(f"%{q}%"))
        
        if sort == 'date':
            query = query.order_by(Event.starts_at.asc())
        elif sort == 'price':
            query = query.order_by(Event.min_price.asc())
        elif sort == 'capacity':
            query = query.order_by(Event.available.asc())
        
        offset = (page - 1) * page_size
        total = query.count()
        events = query.offset(offset).limit(page_size).all()
        
        return {
            'count': total,
            'page': page,
            'results': [self._serialize_event(e) for e in events]
        }
    
    def get_event_detail(self, event_id: UUID):
        event = self.db.query(Event).options(
            joinedload(Event.venue)
        ).filter(Event.id == event_id).first()
        
        if not event:
            return None
        
        ticket_types = self.db.query(TicketType).filter(TicketType.event_id == event_id).all()
        
        return {
            'id': str(event.id),
            'title': event.title,
            'starts_at': event.starts_at.isoformat() if event.starts_at is not None else None,
            'description': event.description,
            'min_price': float(event.min_price) if event.min_price is not None else None, # type: ignore
            'total_capacity': event.total_capacity,
            'available': event.available,
            'venue': {
                'id': str(event.venue.id),
                'name': event.venue.name,
                'city': event.venue.city
            } if event.venue else None,
            'tiers': [self._serialize_ticket_type(tt) for tt in ticket_types]
        }
    
    def _serialize_event(self, event):
        # Acceder a los valores directamente desde el objeto
        # SQLAlchemy ya los tiene como atributos normales
        starts_at = event.starts_at
        min_price = event.min_price
        
        return {
            'id': str(event.id),
            'title': event.title,
            'starts_at': starts_at.isoformat() if starts_at is not None else None,
            'min_price': float(min_price) if min_price is not None else None,
            'total_capacity': event.total_capacity,
            'available': event.available,
            'venue': {
                'id': str(event.venue.id),
                'name': event.venue.name,
                'city': event.venue.city
            } if event.venue else None
        }
    
    def _serialize_ticket_type(self, tt):
        price = tt.price
        return {
            'id': str(tt.id),
            'name': tt.name,
            'price': float(price) if price is not None else None,
            'total_capacity': tt.total_capacity,
            'available': tt.available
        }


# Import needed for joinedload
from sqlalchemy.orm import joinedload