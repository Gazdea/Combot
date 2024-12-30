from typing import Generic, List, Optional, Type, TypeVar
from sqlalchemy.orm import Session

from app.config.log_execution import log_execution, log_class
from app.db.repository import BaseRepository

T = TypeVar('T')

@log_class
class BaseRepositoryImpl(BaseRepository, Generic[T]):
    def __init__(self, model: Type[T], session: Session):
        self.model = model
        self.session: Session = session

    def add_if_not_exists(self, instance: T) -> Optional[T]:
        if not self.session.query(self.model).filter_by(id=instance.id).first():
            self.session.add(instance)
            self.session.flush()
            self.session.commit()
            return instance
        return None

    def add(self, instance: T) -> Optional[T]:
        self.session.add(instance)
        self.session.flush()
        self.session.commit()
        return instance

    def update(self, instance: T) -> Optional[T]:
        self.session.merge(instance)
        self.session.flush()
        self.session.commit()
        return instance

    def get(self, entity_id: int) -> Optional[T]:
        return self.session.query(self.model).filter(self.model.id == entity_id).first()

    def list(self) -> List[T]:
        return self.session.query(self.model).all()

    def delete(self, entity_id: int) -> bool:
        if instance := self.session.query(self.model).filter(self.model.id == entity_id).first():
            self.session.delete(instance)
            self.session.commit()
            return True
        return False

