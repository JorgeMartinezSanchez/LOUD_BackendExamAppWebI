from typing import Dict, Any, List
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import update
from models.models import TicketType
from base_repository import BaseRepository
from repositories.interfaces import ITicketTypeRepository

class TicketTypeRepository(BaseRepository[TicketType], ITicketTypeRepository):
    """Cumple SRP: solo responsabilidad de acceso a datos de TicketType"""
    
    def __init__(self, db: Session):
        super().__init__(db, TicketType)
    
    def _apply_filters(self, query, filters: Dict[str, Any]):
        if filters.get('event_id'):
            query = query.filter(TicketType.event_id == filters['event_id'])
        return query
    
    def _apply_ordering(self, query, sort: str):
        return query.order_by(TicketType.price.asc())
    
    # Métodos específicos de la interfaz
    def decrease_availability(self, ticket_type_id: UUID, quantity: int = 1) -> bool:
        result = self.db.execute(
            update(TicketType)
            .where(TicketType.id == ticket_type_id)
            .where(TicketType.available >= quantity)
            .values(available=TicketType.available - quantity)
        )
        self.db.commit()
        return result.rowcount > 0
    
    def increase_availability(self, ticket_type_id: UUID, quantity: int = 1) -> bool:
        result = self.db.execute(
            update(TicketType)
            .where(TicketType.id == ticket_type_id)
            .where(TicketType.available + quantity <= TicketType.total_capacity)
            .values(available=TicketType.available + quantity)
        )
        self.db.commit()
        return result.rowcount > 0