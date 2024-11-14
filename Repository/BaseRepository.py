from typing import Optional, Type, TypeVar
from config import session_scope
from sqlalchemy.orm import make_transient

T = TypeVar('T')

class BaseRepository:
    def __init__(self, model: Type[T]):
        self.model = model

    def save(self, instance: T) -> Optional[T]:
        """Save or update an instance of the model.
        
        Args:
            instance (T): The instance to save.
        
        Returns:
            Optional[T]: The saved instance, or None if the instance could not be saved.
        """
        with session_scope() as session:
            instance = session.merge(instance)
            session.flush()
            session.refresh(instance)
            session.expunge(instance)
            make_transient(instance)
            return instance

    def get(self, entity_id: int) -> Optional[T]:
        """
        Get an instance of the model by its id.

        Args:
            entity_id (int): The id of the instance to retrieve.

        Returns:
            Optional[T]: The instance if found, otherwise None.
        """
        with session_scope() as session:
            instance = session.query(self.model).filter(self.model.id == entity_id).first()
            if instance:
                session.expunge(instance)
                make_transient(instance)
            return instance

    def list(self) -> list[T]:
        """Retrieve all instances of the model.

        Returns:
            list[T]: A list of all instances of the model.
        """
        with session_scope() as session:
            instances = session.query(self.model).all()
            for instance in instances:
                session.expunge(instance)
                make_transient(instance)
            return instances

    def delete(self, entity_id: int) -> Optional[bool]:
        """Delete an instance of the model by its id.
        
        Args:
            entity_id (int): The id of the instance to delete.
        
        Returns:
            Optional[bool]: True if the instance was deleted, False if the instance could not be found.
        """
        with session_scope() as session:
            instance = session.query(self.model).filter(self.model.id == entity_id).first()
            if instance:
                session.delete(instance)
                return True
            return False

