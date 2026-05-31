from typing import List
from src.application.queries.get_available_events_query import GetAvailableEventsQuery
from src.application.dtos.event_dto import EventDTO
from src.application.interfaces.event_query_service import EventQueryService

class GetAvailableEventsHandler:
    def __init__(self, query_service: EventQueryService):
        self.query_service = query_service

    def handle(self, query: GetAvailableEventsQuery) -> List[EventDTO]:
        return self.query_service.get_published_events()
    