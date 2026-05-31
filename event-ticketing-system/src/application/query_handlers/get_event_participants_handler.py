from typing import List
from src.application.queries.get_event_participants_query import GetEventParticipantsQuery
from src.application.dtos.participant_dto import ParticipantDTO
from src.application.interfaces.event_query_service import EventQueryService

class GetEventParticipantsHandler:
    def __init__(self, query_service: EventQueryService):
        self.query_service = query_service

    def handle(self, query: GetEventParticipantsQuery) -> List[ParticipantDTO]:
        return self.query_service.get_event_participants(query.event_id)