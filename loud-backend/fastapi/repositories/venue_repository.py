from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func
from models.models import Venue, Event

class VenueRepository:
    """Repositorio para venues usando SQLAlchemy"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, venue_id: str) -> Optional[Venue]:
        return self.db.query(Venue).filter(Venue.id == venue_id).first()
    
    def list(self, filters: Dict[str, Any], limit: int, offset: int) -> List[Venue]:
        query = self.db.query(Venue)
        
        if filters.get('city'):
            query = query.filter(Venue.city == filters['city'])
        
        if filters.get('name'):
            query = query.filter(Venue.name.ilike(f"%{filters['name']}%"))
        
        return query.order_by(Venue.name.asc()).offset(offset).limit(limit).all()
    
    def count(self, filters: Dict[str, Any]) -> int:
        query = self.db.query(func.count(Venue.id))
        
        if filters.get('city'):
            query = query.filter(Venue.city == filters['city'])
        
        if filters.get('name'):
            query = query.filter(Venue.name.ilike(f"%{filters['name']}%"))
        
        return query.scalar() or 0
    
    def create(self, data: Dict[str, Any]) -> Venue:
        venue = Venue(**data)
        self.db.add(venue)
        self.db.commit()
        self.db.refresh(venue)
        return venue
    
    def update(self, venue_id: str, data: Dict[str, Any]) -> Optional[Venue]:
        venue = self.get_by_id(venue_id)
        if not venue:
            return None
        
        for key, value in data.items():
            if hasattr(venue, key) and value is not None:
                setattr(venue, key, value)
        
        self.db.commit()
        self.db.refresh(venue)
        return venue
    
    def delete(self, venue_id: str) -> bool:
        venue = self.get_by_id(venue_id)
        if not venue:
            return False
        
        self.db.delete(venue)
        self.db.commit()
        return True
    
    def get_events_by_venue(self, venue_id: str, limit: int = 10) -> List[Event]:
        return self.db.query(Event).filter(
            Event.venue_id == venue_id,
            Event.starts_at > func.now()
        ).order_by(Event.starts_at.asc()).limit(limit).all()
    
    def get_cities(self) -> List[str]:
        results = self.db.query(Venue.city.distinct()).order_by(Venue.city.asc()).all()
        return [row[0] for row in results]