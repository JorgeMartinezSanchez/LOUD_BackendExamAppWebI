from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any, TypeVar, Generic
from uuid import UUID

T = TypeVar('T')

# Interface segregada - solo lectura
class IReadRepository(ABC, Generic[T]):
    @abstractmethod
    def get_by_id(self, id: UUID) -> Optional[T]:
        pass
    
    @abstractmethod
    def list(self, filters: Dict[str, Any], limit: int, offset: int) -> List[T]:
        pass
    
    @abstractmethod
    def count(self, filters: Dict[str, Any]) -> int:
        pass

# Interface segregada - escritura
class IWriteRepository(ABC, Generic[T]):
    @abstractmethod
    def create(self, data: Dict[str, Any]) -> T:
        pass
    
    @abstractmethod
    def update(self, id: UUID, data: Dict[str, Any]) -> Optional[T]:
        pass
    
    @abstractmethod
    def delete(self, id: UUID) -> bool:
        pass

# Interface completa (combina ambas)
class IRepository(IReadRepository[T], IWriteRepository[T], ABC):
    pass

# Interface específica para Event (Open/Closed)
class IEventRepository(IRepository):
    @abstractmethod
    def get_upcoming(self, limit: int) -> List[T]:
        pass
    
    @abstractmethod
    def search_by_title(self, query: str, limit: int, offset: int) -> List[T]:
        pass
    
    @abstractmethod
    def update_availability_from_tiers(self, event_id: UUID) -> None:
        pass

# Interface específica para TicketType
class ITicketTypeRepository(IRepository):
    @abstractmethod
    def decrease_availability(self, ticket_type_id: UUID, quantity: int) -> bool:
        pass
    
    @abstractmethod
    def increase_availability(self, ticket_type_id: UUID, quantity: int) -> bool:
        pass

# Interfaz para Ticket
class ITicketRepository(IRepository[T]):
    @abstractmethod
    def get_by_order(self, order_id: UUID) -> List[T]:
        """Obtener todos los tickets de una orden"""
        pass
    
    @abstractmethod
    def get_by_ticket_type(self, ticket_type_id: UUID) -> List[T]:
        """Obtener todos los tickets de un tipo"""
        pass
    
    @abstractmethod
    def create_batch(self, tickets_data: List[Dict[str, Any]]) -> List[T]:
        """Crear múltiples tickets a la vez"""
        pass

class IOrderRepository(IRepository[T]):
    @abstractmethod
    def get_by_customer_email(self, email: str, limit: int, offset: int) -> List[T]:
        pass
    
    @abstractmethod
    def get_pending_orders(self) -> List[T]:
        pass
    
    @abstractmethod
    def update_status(self, order_id: UUID, status: str) -> Optional[T]:
        pass
    
    @abstractmethod
    def calculate_total(self, order_id: UUID) -> float:
        pass
    
    @abstractmethod
    def update_total(self, order_id: UUID) -> Optional[T]:  # ← AGREGAR ESTO
        pass