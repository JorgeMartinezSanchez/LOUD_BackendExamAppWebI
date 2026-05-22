from repositories.order_repository import OrderRepository

_order_repository: OrderRepository = None

def get_order_repository() -> OrderRepository:
    """Dependencia de FastAPI para el repositorio de orders"""
    global _order_repository
    if _order_repository is None:
        _order_repository = OrderRepository()
    return _order_repository