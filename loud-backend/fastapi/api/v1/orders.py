from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from dependencies.get_db import get_db
from services.order_service import OrderService

router = APIRouter(prefix="/api/v1", tags=["orders"])

@router.post("/orders/")
def create_order(
    customer_name: str,
    customer_email: str,
    db: Session = Depends(get_db)
):
    service = OrderService(db)
    return service.create_order(customer_name, customer_email)

@router.get("/orders/{order_id}")
def get_order(
    order_id: UUID,
    db: Session = Depends(get_db)
):
    service = OrderService(db)
    result = service.get_order(order_id)
    if not result:
        raise HTTPException(status_code=404, detail="Order not found")
    return result