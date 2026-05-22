from typing import Dict, Any, List, Optional
from uuid import UUID
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, and_
from models.order import Order
from models.ticket import Ticket
from models.ticket_type import TicketType
from repositories.base_repository import BaseRepository
from repositories.interfaces import IOrderRepository

class OrderRepository(BaseRepository[Order], IOrderRepository):
    """Repositorio para Orders"""
    
    def __init__(self, db: Session):
        super().__init__(db, Order)
    
    def get_by_id(self, id: UUID) -> Optional[Order]:
        return self.db.query(Order).options(
            joinedload(Order.tickets).joinedload(Ticket.ticket_type)
        ).filter(Order.id == id).first()
    
    def _apply_filters(self, query, filters: Dict[str, Any]):
        if filters.get('status'):
            query = query.filter(Order.status == filters['status'])
        
        if filters.get('customer_email'):
            query = query.filter(Order.customer_email.ilike(f"%{filters['customer_email']}%"))
        
        if filters.get('date_from'):
            query = query.filter(Order.created_at >= filters['date_from'])
        
        if filters.get('date_to'):
            query = query.filter(Order.created_at <= filters['date_to'])
        
        return query
    
    def _apply_ordering(self, query, sort: str):
        order_map = {
            'date': Order.created_at.desc(),
            'total': Order.total.desc(),
            'customer': Order.customer_name.asc(),
        }
        order_by = order_map.get(sort, Order.created_at.desc())
        return query.order_by(order_by)
    
    # Métodos específicos
    def get_by_customer_email(self, email: str, limit: int, offset: int) -> List[Order]:
        return self.db.query(Order).filter(
            Order.customer_email.ilike(f"%{email}%")
        ).offset(offset).limit(limit).all()
    
    def get_pending_orders(self) -> List[Order]:
        return self.db.query(Order).filter(
            Order.status == 'pending'
        ).order_by(Order.created_at.asc()).all()
    
    def update_status(self, order_id: UUID, status: str) -> Optional[Order]:
        from sqlalchemy import update
        
        result = self.db.execute(
            update(Order)
            .where(Order.id == order_id)
            .values(status=status)
        )
        self.db.commit()
        
        if result.rowcount == 0:
            return None
        
        return self.get_by_id(order_id)
    
    def calculate_total(self, order_id: UUID) -> float:
        """Calcula el total sumando precios de ticket_types"""
        result = self.db.query(
            func.coalesce(func.sum(TicketType.price), 0)
        ).join(
            Ticket, Ticket.ticket_type_id == TicketType.id
        ).filter(
            Ticket.order_id == order_id
        ).scalar() or 0
        
        return float(result)
    
    def update_total(self, order_id: UUID) -> Optional[Order]:
        """Actualiza el total de la orden"""
        total = self.calculate_total(order_id)
        
        self.db.query(Order).filter(Order.id == order_id).update(
            {'total': total}
        )
        self.db.commit()
        
        return self.get_by_id(order_id)