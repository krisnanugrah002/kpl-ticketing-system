import uuid
from typing import Optional
from sqlalchemy.orm import Session
from decimal import Decimal
from src.domain.repositories.event_repository import EventRepository
from src.domain.aggregates.event import Event, EventStatus
from src.domain.entities.ticket_category import TicketCategory
from src.domain.value_objects.date_range import DateRange
from src.domain.value_objects.money import Money
from src.infrastructure.database.models.event_model import EventModel, TicketCategoryModel

class EventRepositoryImpl(EventRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, event: Event) -> None:
        event_model = self.session.query(EventModel).filter_by(id=event.id).first()
        
        if not event_model:
            event_model = EventModel(id=event.id)
            self.session.add(event_model)

        event_model.name = event.name
        event_model.description = event.description
        event_model.location = event.location
        event_model.max_capacity = event.max_capacity
        event_model.start_date = event.date_range.start_date
        event_model.end_date = event.date_range.end_date
        event_model.status = event.status.value

        for category in event.categories:
            cat_model = self.session.query(TicketCategoryModel).filter_by(id=category.id).first()
            if not cat_model:
                cat_model = TicketCategoryModel(id=category.id, event_id=event.id)
                self.session.add(cat_model)
            
            cat_model.name = category.name
            cat_model.price = category.price.amount
            cat_model.quota = category.quota
            cat_model.sales_start_date = category.sales_period.start_date
            cat_model.sales_end_date = category.sales_period.end_date

        self.session.commit()

    def get_by_id(self, id: uuid.UUID) -> Optional[Event]:
        event_model = self.session.query(EventModel).filter_by(id=id).first()
        if not event_model:
            return None

        date_range = DateRange(start_date=event_model.start_date, end_date=event_model.end_date)
        event = Event(
            id=event_model.id,
            name=event_model.name,
            description=event_model.description,
            location=event_model.location,
            max_capacity=event_model.max_capacity,
            date_range=date_range
        )
        event.status = EventStatus(event_model.status)

        for cat_model in event_model.categories:
            sales_period = DateRange(start_date=cat_model.sales_start_date, end_date=cat_model.sales_end_date)
            price = Money(amount=Decimal(str(cat_model.price)))
            category = TicketCategory(
                id=cat_model.id,
                name=cat_model.name,
                price=price,
                quota=cat_model.quota,
                sales_period=sales_period
            )
            event.categories.append(category)

        return event