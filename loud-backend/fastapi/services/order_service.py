from typing import Optional, Dict, Any, List
from uuid import UUID
from fastapi import Depends
from sqlalchemy.orm import Session
from core.database import get_db
from repositories.interfaces import IOrderRepository, ITicketRepository, ITicketTypeRepository
from repositories.order_repository import OrderRepository
from repositories.ticket_repository import TicketRepository
from repositories.ticket_type_repository import TicketTypeRepository

class OrderService:
    """Servicio para Orders - lógica de negocio de compras"""
    
    def __init__(
        self,
        order_repo: IOrderRepository,
        ticket_repo: ITicketRepository,
        ticket_type_repo: ITicketTypeRepository
    ):
        self.order_repo = order_repo
        self.ticket_repo = ticket_repo
        self.ticket_type_repo = ticket_type_repo
    
    def create_order(self, customer_name: str, customer_email: str) -> Dict[str, Any]:
        """Crear una nueva orden vacía"""
        order = self.order_repo.create({
            'customer_name': customer_name,
            'customer_email': customer_email,
            'total': 0.0,
            'status': 'pending'
        })
        
        return {
            'id': order.id,
            'customer_name': order.customer_name,
            'customer_email': order.customer_email,
            'total': order.total,
            'status': order.status
        }
    
    def add_ticket_to_order(self, order_id: UUID, ticket_type_id: UUID, participant_name: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Agregar un ticket a una orden"""
        # Verificar disponibilidad
        ticket_type = self.ticket_type_repo.get_by_id(ticket_type_id)
        if not ticket_type or ticket_type.available <= 0:
            return None
        
        # Disminuir disponibilidad
        success = self.ticket_type_repo.decrease_availability(ticket_type_id, 1)
        if not success:
            return None
        
        # Crear ticket
        ticket = self.ticket_repo.create({
            'order_id': order_id,
            'ticket_type_id': ticket_type_id,
            'participant_name': participant_name
        })
        
        # Actualizar total de la orden
        self.order_repo.update_total(order_id)
        
        return {
            'id': ticket.id,
            'ticket_type_id': ticket.ticket_type_id,
            'participant_name': ticket.participant_name
        }
    
    def confirm_order(self, order_id: UUID) -> Optional[Dict[str, Any]]:
        """Confirmar una orden (cambiar estado a confirmed)"""
        order = self.order_repo.update_status(order_id, 'confirmed')
        if not order:
            return None
        
        return {
            'id': order.id,
            'status': order.status,
            'total': order.total
        }
    
    def cancel_order(self, order_id: UUID) -> Optional[Dict[str, Any]]:
        """Cancelar una orden y liberar tickets"""
        order = self.order_repo.get_by_id(order_id)
        if not order or order.status != 'pending':
            return None
        
        # Liberar tickets (aumentar disponibilidad)
        tickets = self.ticket_repo.get_by_order(order_id)
        for ticket in tickets:
            self.ticket_type_repo.increase_availability(ticket.ticket_type_id, 1)
        
        # Eliminar tickets
        for ticket in tickets:
            self.ticket_repo.delete(ticket.id)
        
        # Cambiar estado de la orden
        updated_order = self.order_repo.update_status(order_id, 'cancelled')
        if not updated_order:
            return None
        
        return {
            'id': updated_order.id,
            'status': updated_order.status
        }
    
    def get_order(self, order_id: UUID) -> Optional[Dict[str, Any]]:
        """Obtener orden con todos sus tickets"""
        order = self.order_repo.get_by_id(order_id)
        if not order:
            return None
        
        tickets = []
        for ticket in order.tickets:
            tickets.append({
                'id': ticket.id,
                'ticket_type_name': ticket.ticket_type.name,
                'price': ticket.ticket_type.price,
                'participant_name': ticket.participant_name
            })
        
        return {
            'id': order.id,
            'customer_name': order.customer_name,
            'customer_email': order.customer_email,
            'total': order.total,
            'status': order.status,
            'tickets': tickets
        }

# Factory
def get_order_service(db: Session = Depends(get_db)) -> OrderService:
    return OrderService(
        order_repo=OrderRepository(db),
        ticket_repo=TicketRepository(db),
        ticket_type_repo=TicketTypeRepository(db)
    )