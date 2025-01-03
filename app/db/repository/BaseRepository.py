from abc import ABC, abstractmethod
from typing import Generic, Optional, TypeVar

T = TypeVar('T')

class BaseRepository(ABC, Generic[T]):


    @abstractmethod
    def add_if_not_exists(self, instance: T) -> Optional[T]:
        """Add an instance of the model if it does not already exist.

        Args:
            instance (T): The instance to add.

        Returns:
            Optional[T]: The added instance, or None if the instance already exists.
        """
        raise NotImplementedError()

    @abstractmethod
    def add(self, instance: T) -> Optional[T]:
        """Save or update an instance of the model.
        
        Args:
            instance (T): The instance to save.
        
        Returns:
            Optional[T]: The saved instance, or None if the instance could not be saved.
        """
        raise NotImplementedError()

    @abstractmethod
    def update(self, instance: T) -> Optional[T]:
        """Update an instance of the model.

        Args:
            instance (T): The instance to update.

        Returns:
            Optional[T]: The updated instance, or None if the instance could not be updated.
        """
        raise NotImplementedError()

    @abstractmethod
    def get(self, entity_id: int) -> Optional[T]:
        """
        Get an instance of the model by its id.

        Args:
            entity_id (int): The id of the instance to retrieve.

        Returns:
            Optional[T]: The instance if found, otherwise None.
        """
        raise NotImplementedError()

    @abstractmethod
    def list(self) -> list[T]:
        """Retrieve all instances of the model.

        Returns:
            list[T]: A list of all instances of the model.
        """
        raise NotImplementedError()

    @abstractmethod
    def delete(self, entity_id: int) -> bool:
        """Delete an instance of the model by its id.
        
        Args:
            entity_id (int): The id of the instance to delete.
        
        Returns:
            Optional[bool]: True if the instance was deleted, False if the instance could not be found.
        """
        raise NotImplementedError()

