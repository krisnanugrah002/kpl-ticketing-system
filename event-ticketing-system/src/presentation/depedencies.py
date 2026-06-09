from fastapi import Depends
from sqlalchemy.orm import Session
from src.infrastructure.database.session import get_session
from src.infrastructure.repositories.event_repository_impl import EventRepositoryImpl
from src.infrastructure.repositories.ticket_repository_impl import TicketRepositoryImpl
from src.infrastructure.services.event_query_service_impl import EventQueryServiceImpl
from src.application.command_handlers.create_event_handler import CreateEventHandler
from src.application.command_handlers.publish_event_handler import PublishEventHandler
from src.application.command_handlers.check_in_handler import CheckInHandler
from src.application.query_handlers.get_available_events_handler import GetAvailableEventsHandler
from src.application.query_handlers.get_event_participants_handler import GetEventParticipantsHandler

def get_event_repository(session: Session = Depends(get_session)) -> EventRepositoryImpl:
    return EventRepositoryImpl(session)

def get_ticket_repository(session: Session = Depends(get_session)) -> TicketRepositoryImpl:
    return TicketRepositoryImpl(session)

def get_event_query_service(session: Session = Depends(get_session)) -> EventQueryServiceImpl:
    return EventQueryServiceImpl(session)

def get_create_event_handler(repository: EventRepositoryImpl = Depends(get_event_repository)) -> CreateEventHandler:
    return CreateEventHandler(repository)

def get_publish_event_handler(repository: EventRepositoryImpl = Depends(get_event_repository)) -> PublishEventHandler:
    return PublishEventHandler(repository)

def get_check_in_handler(repository: TicketRepositoryImpl = Depends(get_ticket_repository)) -> CheckInHandler:
    return CheckInHandler(repository)

def get_available_events_handler(query_service: EventQueryServiceImpl = Depends(get_event_query_service)) -> GetAvailableEventsHandler:
    return GetAvailableEventsHandler(query_service)

def get_event_participants_handler(query_service: EventQueryServiceImpl = Depends(get_event_query_service)) -> GetEventParticipantsHandler:
    return GetEventParticipantsHandler(query_service)