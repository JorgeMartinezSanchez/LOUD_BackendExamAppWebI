from typing import Optional, Dict, Any
from uuid import UUID
import datetime
from datetime import UTC
from sqlalchemy.orm import Session, joinedload
from models.models import Event, Venue, TicketType
from cache.cache_service import cache # type: ignore

class EventService:
    
    def __init__(self, db: Session):
        self.db = db
    
    def list_events(self, q: Optional[str], sort: str, page: int, page_size: int) -> Dict[str, Any]:
        # Cache key única para esta consulta
        cache_key = f"events:list:{q}:{sort}:{page}:{page_size}"
        
        # Intentar obtener del caché
        cached = cache.get(cache_key)
        if cached:
            return cached
        
        # Si no está en caché, consultar DB
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
        
        result = {
            'count': total,
            'page': page,
            'results': [self._serialize_event(e) for e in events]
        }
        
        # Guardar en caché (TTL 60 segundos)
        cache.set(cache_key, result, ttl=60)
        
        return result
    
    def get_event_detail(self, event_id: UUID):
        cache_key = f"events:detail:{event_id}"
        
        # Intentar obtener del caché
        cached = cache.get(cache_key)
        if cached:
            return cached
        
        # Si no está en caché, consultar DB
        event = self.db.query(Event).options(
            joinedload(Event.venue)
        ).filter(Event.id == event_id).first()
        
        if not event:
            return None
        
        ticket_types = self.db.query(TicketType).filter(TicketType.event_id == event_id).all()
        
        result = {
            'id': str(event.id),
            'title': event.title,
            'hour_change': event.hour_change,
            'starts_at': event.starts_at.isoformat() if event.starts_at else None, # type: ignore
            'description': event.description,
            'min_price': float(event.min_price) if event.min_price else None, # type: ignore
            'total_capacity': event.total_capacity,
            'available': event.available,
            'venue': {
                'id': str(event.venue.id),
                'name': event.venue.name,
                'city': event.venue.city
            } if event.venue else None,
            'tiers': [self._serialize_ticket_type(tt) for tt in ticket_types]
        }
        
        # Guardar en caché (TTL 60 segundos)
        cache.set(cache_key, result, ttl=60)
        
        return result
    
    def _serialize_event(self, event):
        return {
            'id': str(event.id),
            'title': event.title,
            'hour_change': event.hour_change,
            'starts_at': event.starts_at.isoformat() if event.starts_at else None,
            'min_price': float(event.min_price) if event.min_price else None,
            'total_capacity': event.total_capacity,
            'available': event.available,
            'venue': {
                'id': str(event.venue.id),
                'name': event.venue.name,
                'city': event.venue.city
            } if event.venue else None
        }
    
    def _serialize_ticket_type(self, tt):
        return {
            'id': str(tt.id),
            'name': tt.name,
            'price': float(tt.price) if tt.price else None,
            'total_capacity': tt.total_capacity,
            'available': tt.available
        }
    
    def price_update(self, event: Event) :
        if (event.hour_change >= datetime.UTC.):
            query = self.db.query(Event).