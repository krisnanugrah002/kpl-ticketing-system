import uuid
from abc import ABC, abstractmethod
from typing import List
from src.application.dtos.event_dto import EventDTO
from src.application.dtos.participant_dto import ParticipantDTO

class EventQueryService(ABC):
    @abstractmethod
    def get_published_events(self) -> List[EventDTO]:
        pass
        
    @abstractmethod
    def get_event_participants(self, event_id: uuid.UUID) -> List[ParticipantDTO]:
        pass