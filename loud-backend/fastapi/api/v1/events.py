from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID
from dependencies.get_db import get_db
from services.event_service import EventService

router = APIRouter(prefix="/api/v1", tags=["events"])

@router.get("/events/")
def list_events(
    q: Optional[str] = Query(None),
    sort: str = Query("date"),
    page: int = Query(1, ge=1),
    page_size: int = Query(9, ge=1, le=50),
    db: Session = Depends(get_db)
):
    service = EventService(db)
    return service.list_events(q, sort, page, page_size)

@router.get("/events/{event_id}")
def get_event(
    event_id: UUID,
    db: Session = Depends(get_db)
):
    service = EventService(db)

    return service.get_event_detail(event_id)

@router.get("/events/{event_id}/price-history")
def price_history(
    event_id: UUID,
    db: Session = Depends(get_db)
){
    
}