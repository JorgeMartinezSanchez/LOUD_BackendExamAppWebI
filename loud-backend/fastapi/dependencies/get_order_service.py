from fastapi import Depends
from services.order_service import OrderService
from dependencies.get_order_repository import get_order_repository
from repositories.order_repository import OrderRepository

def get_order_service(
    repository: OrderRepository = Depends(get_order_repository)
) -> OrderService:
    """Dependencia de FastAPI para el servicio de orders"""
    return OrderService(repository)