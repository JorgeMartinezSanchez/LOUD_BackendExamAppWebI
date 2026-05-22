from typing import Dict, Any, Optional, List, Type, Generic, TypeVar
from uuid import UUID
from sqlalchemy.orm import Session, Query, class_mapper
from sqlalchemy import func

ModelType = TypeVar('ModelType')

class BaseRepository(Generic[ModelType]):
    """
    Clase base con implementación común.
    """
    
    def __init__(self, db: Session, model: Type[ModelType]):
        self.db = db
        self.model = model
        self.pk_column = class_mapper(model).primary_key[0]
    
    def get_by_id(self, id: UUID) -> Optional[ModelType]:
        return self.db.query(self.model).filter(self.pk_column == id).first()
    
    def list(self, filters: Dict[str, Any], limit: int, offset: int) -> List[ModelType]:
        query = self.db.query(self.model)
        
        query = self._apply_filters(query, filters)
        query = self._apply_ordering(query, filters.get('sort', 'id'))
        
        return query.offset(offset).limit(limit).all()
    
    def count(self, filters: Dict[str, Any]) -> int:
        query = self.db.query(func.count(self.pk_column))
        query = self._apply_filters(query, filters)
        return query.scalar() or 0
    
    def create(self, data: Dict[str, Any]) -> ModelType:
        instance = self.model(**data)
        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)
        return instance
    
    def update(self, id: UUID, data: Dict[str, Any]) -> Optional[ModelType]:
        instance = self.get_by_id(id)
        if not instance:
            return None
        
        for key, value in data.items():
            if hasattr(instance, key) and value is not None:
                setattr(instance, key, value)
        
        self.db.commit()
        self.db.refresh(instance)
        return instance
    
    def delete(self, id: UUID) -> bool:
        instance = self.get_by_id(id)
        if not instance:
            return False
        
        self.db.delete(instance)
        self.db.commit()
        return True
    
    def _apply_filters(self, query: Query, filters: Dict[str, Any]) -> Query:
        """Hook para aplicar filtros específicos"""
        return query
    
    def _apply_ordering(self, query: Query, sort: str) -> Query:
        """Hook para aplicar ordenamiento específico"""
        return query.order_by(self.pk_column)