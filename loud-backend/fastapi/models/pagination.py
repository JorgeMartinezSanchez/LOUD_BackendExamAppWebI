from pydantic import BaseModel, Field
from typing import TypeVar, Generic, List

T = TypeVar('T')

class PaginatedResponse(BaseModel, Generic[T]):
    count: int = Field(..., description="Total number of items")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Number of items per page")
    total_pages: int = Field(..., description="Total number of pages")
    results: List[T] = Field(default_factory=list, description="Items for current page")