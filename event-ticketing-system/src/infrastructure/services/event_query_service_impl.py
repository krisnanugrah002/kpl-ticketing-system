import uuid
from typing import List
from sqlalchemy.orm import Session
from src.application.interfaces.event_query_service import EventQueryService
from src.application.dtos.event_dto import EventDTO, TicketCategoryDTO
from src.application.dtos.participant_dto import ParticipantDTO
from src.infrastructure.database.models.event_model import EventModel, TicketCategoryModel
from src.infrastructure.database.models.ticket_model import TicketModel

class EventQueryServiceImpl(EventQueryService):
    def __init__(self, session: Session):
        self.session = session

    def get_published_events(self) -> List[EventDTO]:
        events = self.session.query(EventModel).filter(EventModel.status == "Published").all()
        result = []
        
        for event in events:
            categories_dto = []
            for cat in event.categories:
                categories_dto.append(
                    TicketCategoryDTO(
                        id=cat.id,
                        name=cat.name,
                        price=float(cat.price),
                        quota=cat.quota,
                        sales_start_date=cat.sales_start_date,
                        sales_end_date=cat.sales_end_date,
                        is_active=True
                    )
                )
            
            event_dto = EventDTO(
                id=event.id,
                name=event.name,
                description=event.description,
                location=event.location,
                max_capacity=event.max_capacity,
                start_date=event.start_date,
                end_date=event.end_date,
                status=event.status,
                categories=categories_dto
            )
            result.append(event_dto)
            
        return result

    def get_event_participants(self, event_id: uuid.UUID) -> List[ParticipantDTO]:
        query = self.session.query(TicketModel, TicketCategoryModel).join(
            TicketCategoryModel, TicketModel.category_id == TicketCategoryModel.id
        ).filter(
            TicketModel.event_id == event_id
        ).all()
        
        participants = []
        for ticket, category in query:
            participants.append(
                ParticipantDTO(
                    ticket_id=ticket.id,
                    ticket_code=ticket.code,
                    category_name=category.name,
                    status=ticket.status
                )
            )
            
        return participants