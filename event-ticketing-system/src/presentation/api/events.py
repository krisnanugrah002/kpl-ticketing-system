import uuid
from alembic.util import status
from fastapi import APIRouter, Depends, HTTPException
from typing import List

from src.presentation.schemas.event_schema import EventCreate
from src.application.commands.create_event_command import CreateEventCommand, TicketCategoryCommandData
from src.application.commands.publish_event_command import PublishEventCommand
from src.application.queries.get_available_events_query import GetAvailableEventsQuery
from src.application.queries.get_event_participants_query import GetEventParticipantsQuery

from src.application.command_handlers.create_event_handler import CreateEventHandler
from src.application.command_handlers.publish_event_handler import PublishEventHandler
from src.application.query_handlers.get_available_events_handler import GetAvailableEventsHandler
from src.application.query_handlers.get_event_participants_handler import GetEventParticipantsHandler

from src.application.commands.cancel_event_command import CancelEventCommand
from src.application.command_handlers.cancel_event_handler import CancelEventHandler

from src.application.commands.disable_ticket_category_command import DisableTicketCategoryCommand
from src.application.command_handlers.disable_ticket_category_handler import DisableTicketCategoryHandler
from src.application.queries.get_event_details_query import GetEventDetailsQuery
from src.application.query_handlers.get_event_details_handler import GetEventDetailsHandler
from src.presentation.dependencies import get_disable_ticket_category_handler, get_session
from sqlalchemy.orm import Session


from src.presentation.dependencies import (
    get_create_event_handler,
    get_publish_event_handler,
    get_available_events_handler,
    get_event_participants_handler,
    get_cancel_event_handler
)

router = APIRouter(prefix="/events", tags=["Events"])

@router.post("/")
def create_event(
    request: EventCreate,
    handler: CreateEventHandler = Depends(get_create_event_handler)
):
    try:
        categories_data = [
            TicketCategoryCommandData(
                name=cat.name,
                price=cat.price,
                quota=cat.quota,
                sales_start_date=cat.sales_start_date,
                sales_end_date=cat.sales_end_date
            ) for cat in request.categories
        ]
        
        command = CreateEventCommand(
            name=request.name,
            description=request.description,
            location=request.location,
            max_capacity=request.max_capacity,
            start_date=request.start_date,
            end_date=request.end_date,
            categories=categories_data
        )
        event_id = handler.handle(command)
        return {"event_id": event_id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{event_id}/publish")
def publish_event(
    event_id: uuid.UUID,
    handler: PublishEventHandler = Depends(get_publish_event_handler)
):
    try:
        command = PublishEventCommand(event_id=event_id)
        handler.handle(command)
        return {"message": "Event published successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/available")
def get_available_events(
    handler: GetAvailableEventsHandler = Depends(get_available_events_handler)
):
    try:
        query = GetAvailableEventsQuery()
        events = handler.handle(query)
        return events
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{event_id}/participants")
def get_event_participants(
    event_id: uuid.UUID,
    handler: GetEventParticipantsHandler = Depends(get_event_participants_handler)
):
    try:
        query = GetEventParticipantsQuery(event_id=event_id)
        participants = handler.handle(query)
        return participants
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/{event_id}/cancel", status_code=status.HTTP_200_OK)
def cancel_event(
    event_id: uuid.UUID,
    handler: CancelEventHandler = Depends(get_cancel_event_handler)
):
    try:
        command = CancelEventCommand(event_id=event_id)
        handler.handle(command)
        return {"message": "Event cancelled successfully"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/{event_id}/categories/{category_id}/disable", status_code=status.HTTP_200_OK)
def disable_ticket_category(
    event_id: uuid.UUID,
    category_id: uuid.UUID,
    handler: DisableTicketCategoryHandler = Depends(get_disable_ticket_category_handler)
):
    try:
        command = DisableTicketCategoryCommand(event_id=event_id, category_id=category_id)
        handler.handle(command)
        return {"message": "Ticket category disabled successfully"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/{event_id}", status_code=status.HTTP_200_OK)
def get_event_details(
    event_id: uuid.UUID,
    session: Session = Depends(get_session)
):
    try:
        handler = GetEventDetailsHandler(session)
        query = GetEventDetailsQuery(event_id=event_id)
        event = handler.handle(query)
        return event
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))