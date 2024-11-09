from typing import Optional, Type, TypeVar, List
from config import session_scope

T = TypeVar('T')

class BaseRepository:
    def __init__(self, model: Type[T]):
        self.model = model

    def save(self, instance: T) -> Optional[T]:
        with session_scope() as session:
            if not instance.id:
                session.add(instance)
            else:
                session.merge(instance)
            session.commit()
            return instance
        
    def get(self, entity_id: int) -> Optional[T]:
        with session_scope() as session:
            return session.query(self.model).filter(self.model.id == entity_id).first()

    def list(self) -> Optional[List[T]]:
        with session_scope() as session:
            return session.query(self.model).all()

    def update(self, instance: T) -> Optional[T]:
        with session_scope() as session:
            session.merge(instance)
            session.commit()
            return instance

    def delete(self, entity_id: int) -> Optional[bool]:
        with session_scope() as session:
            instance = session.query(self.model).filter(self.model.id == entity_id).first()
            if instance:
                session.delete(instance)
                session.commit()
                return True
            return False