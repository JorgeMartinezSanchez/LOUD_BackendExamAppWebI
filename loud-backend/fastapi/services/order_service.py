from typing import Optional, Dict, Any
from uuid import UUID
from sqlalchemy.orm import Session
from models.order import Order
from models.ticket import Ticket
from models.ticket_type import TicketType

class OrderService:
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_order(self, customer_name: str, customer_email: str) -> Dict[str, Any]:
        order = Order(
            customer_name=customer_name,
            customer_email=customer_email,
            total=0.0,
            status='pending'
        )
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        
        return {
            'id': order.id,
            'customer_name': order.customer_name,
            'customer_email': order.customer_email,
            'total': order.total,
            'status': order.status
        }
    
    def get_order(self, order_id: UUID) -> Optional[Dict[str, Any]]:
        order = self.db.query(Order).filter(Order.id == order_id).first()
        if not order:
            return None
        
        tickets = self.db.query(Ticket).filter(Ticket.order_id == order_id).all()
        
        return {
            'id': order.id,
            'customer_name': order.customer_name,
            'customer_email': order.customer_email,
            'total': order.total,
            'status': order.status,
            'tickets': [{'id': t.id, 'participant_name': t.participant_name} for t in tickets]
        }