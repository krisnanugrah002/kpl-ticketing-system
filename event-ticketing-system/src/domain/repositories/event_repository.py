import uuid
from abc import ABC, abstractmethod
from typing import Optional
from src.domain.aggregates.event import Event

class EventRepository(ABC):
    
    @abstractmethod
    def save(self, event: Event) -> None:
        """
        Saving Event Aggregate data that has been created or updated.
        """
        pass
        
    @abstractmethod
    def get_by_id(self, event_id: uuid.UUID) -> Optional[Event]:
        """
        Retrieving the entire Event Aggregate structure along with its ticket categories
        based on the ID. Returns None if not found.
        """
        pass