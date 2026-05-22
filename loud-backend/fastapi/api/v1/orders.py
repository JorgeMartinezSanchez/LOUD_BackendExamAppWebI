from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from services.order_service import OrderService
from dependencies.get_order_service import get_order_service

router = APIRouter(prefix="/api/v1", tags=["orders"])

@router.post("/orders/")
def create_order(
    customer_name: str,
    customer_email: str,
    service: OrderService = Depends(get_order_service)
):
    return service.create_order(customer_name, customer_email)

@router.post("/orders/{order_id}/tickets")
def add_ticket(
    order_id: UUID,
    ticket_type_id: UUID,
    participant_name: str = "",
    service: OrderService = Depends(get_order_service)
):
    result = service.add_ticket_to_order(order_id, ticket_type_id, participant_name)
    if not result:
        raise HTTPException(status_code=400, detail="Ticket not available")
    return result

@router.post("/orders/{order_id}/confirm")
def confirm_order(
    order_id: UUID,
    service: OrderService = Depends(get_order_service)
):
    result = service.confirm_order(order_id)
    if not result:
        raise HTTPException(status_code=404, detail="Order not found")
    return result

@router.post("/orders/{order_id}/cancel")
def cancel_order(
    order_id: UUID,
    service: OrderService = Depends(get_order_service)
):
    result = service.cancel_order(order_id)
    if not result:
        raise HTTPException(status_code=400, detail="Order cannot be cancelled")
    return result

@router.get("/orders/{order_id}")
def get_order(
    order_id: UUID,
    service: OrderService = Depends(get_order_service)
):
    result = service.get_order(order_id)
    if not result:
        raise HTTPException(status_code=404, detail="Order not found")
    return result