from typing import Optional, Type, TypeVar
from config import session_scope
from sqlalchemy.orm import make_transient

T = TypeVar('T')

class BaseRepository:
    def __init__(self, model: Type[T]):
        self.model = model

    def save(self, instance: T) -> Optional[T]:
        with session_scope() as session:
            if not instance.id:
                session.add(instance)
            else:
                instance = session.merge(instance)
            session.flush()
            session.refresh(instance)
            session.expunge(instance)
            make_transient(instance)
            return instance

    def get(self, entity_id: int) -> Optional[T]:
        with session_scope() as session:
            instance = session.query(self.model).filter(self.model.id == entity_id).first()
            if instance:
                session.expunge(instance)
                make_transient(instance)
            return instance

    def list(self) -> list[T]:
        with session_scope() as session:
            instances = session.query(self.model).all()
            for instance in instances:
                session.expunge(instance)
                make_transient(instance)
            return instances

    def update(self, instance: T) -> Optional[T]:
        with session_scope() as session:
            instance = session.merge(instance)
            session.flush()
            session.refresh(instance)
            session.expunge(instance)
            make_transient(instance)
            return instance

    def delete(self, entity_id: int) -> Optional[bool]:
        with session_scope() as session:
            instance = session.query(self.model).filter(self.model.id == entity_id).first()
            if instance:
                session.delete(instance)
                return True
            return False

