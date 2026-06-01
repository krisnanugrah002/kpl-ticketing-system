import uuid
from abc import ABC, abstractmethod
from typing import Optional
from src.domain.aggregates.ticket import Ticket

class TicketRepository(ABC):
    
    @abstractmethod
    def save(self, ticket: Ticket) -> None:
        pass
        
    @abstractmethod
    def get_by_id(self, ticket_id: uuid.UUID) -> Optional[Ticket]:
        pass

    @abstractmethod
    def get_by_code(self, code: str) -> Optional[Ticket]:
        pass