from typing import Dict, Any, List, Optional
from uuid import UUID
from sqlalchemy.orm import Session, joinedload
from models.ticket import Ticket
from repositories.base_repository import BaseRepository
from repositories.interfaces import ITicketRepository

class TicketRepository(BaseRepository[Ticket], ITicketRepository):
    """Repositorio para Tickets"""
    
    def __init__(self, db: Session):
        super().__init__(db, Ticket)
    
    def get_by_id(self, id: UUID) -> Optional[Ticket]:
        return self.db.query(Ticket).options(
            joinedload(Ticket.order),
            joinedload(Ticket.ticket_type)
        ).filter(Ticket.id == id).first()
    
    def _apply_filters(self, query, filters: Dict[str, Any]):
        if filters.get('order_id'):
            query = query.filter(Ticket.order_id == filters['order_id'])
        
        if filters.get('ticket_type_id'):
            query = query.filter(Ticket.ticket_type_id == filters['ticket_type_id'])
        
        return query
    
    def _apply_ordering(self, query, sort: str):
        return query.order_by(Ticket.created_at.desc())
    
    # Métodos específicos
    def get_by_order(self, order_id: UUID) -> List[Ticket]:
        return self.db.query(Ticket).options(
            joinedload(Ticket.ticket_type)
        ).filter(Ticket.order_id == order_id).all()
    
    def get_by_ticket_type(self, ticket_type_id: UUID) -> List[Ticket]:
        return self.db.query(Ticket).filter(
            Ticket.ticket_type_id == ticket_type_id
        ).all()
    
    def create_batch(self, tickets_data: List[Dict[str, Any]]) -> List[Ticket]:
        """Crear múltiples tickets a la vez"""
        tickets = []
        for data in tickets_data:
            ticket = Ticket(**data)
            self.db.add(ticket)
            tickets.append(ticket)
        
        self.db.commit()
        
        # Refresh each ticket
        for ticket in tickets:
            self.db.refresh(ticket)
        
        return tickets