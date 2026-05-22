from fastapi import APIRouter, Depends, Query
from typing import Optional
from services.event_service import EventService
from dependencies.get_event_service import get_event_service
from models.event import EventResponse, EventDetailResponse
from models.pagination import PaginatedResponse

router = APIRouter(prefix="/api/v1", tags=["events"])

@router.get("/events/", response_model=PaginatedResponse[EventResponse])
def list_events(
    q: Optional[str] = Query(None),
    sort: str = Query("date"),
    page: int = Query(1, ge=1),
    page_size: int = Query(9, ge=1, le=50),
    service: EventService = Depends(get_event_service)  # ← Inyección
):
    return service.list_events(q, sort, page, page_size)

@router.get("/events/{event_id}", response_model=EventDetailResponse)
def get_event(
    event_id: str,
    service: EventService = Depends(get_event_service)  # ← Inyección
):
    return service.get_event_detail(event_id)