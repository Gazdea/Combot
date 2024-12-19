from typing import Generic, List, Optional, Type, TypeVar
from sqlalchemy.orm import Session
from app.db.repository import BaseRepository

T = TypeVar('T')

class BaseRepositoryImpl(BaseRepository, Generic[T]):
    def __init__(self, model: Type[T], session: Session):
        self.model = model
        self.session: Session = session

    def save(self, instance: T) -> Optional[T]:
        if instance := self.session.merge(instance):
            self.session.flush()
            return instance
        return None

    def get(self, entity_id: int) -> Optional[T]:
        return self.session.query(self.model).filter(self.model.id == entity_id).first()

    def list(self) -> List[T]:
        return self.session.query(self.model).all()

    def delete(self, entity_id: int) -> bool:
        if instance := self.session.query(self.model).filter(self.model.id == entity_id).first():
            self.session.delete(instance)
            return True
        return False

