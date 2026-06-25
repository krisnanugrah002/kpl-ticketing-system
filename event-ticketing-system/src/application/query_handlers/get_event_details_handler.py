from sqlalchemy.orm import Session
from src.application.queries.get_event_details_query import GetEventDetailsQuery
from src.infrastructure.database.models.event_model import EventModel

class GetEventDetailsHandler:
    def __init__(self, session: Session):
        self.session = session

    def handle(self, query: GetEventDetailsQuery):
        event = self.session.query(EventModel).filter(EventModel.id == query.event_id).first()
        if not event:
            raise ValueError("Event not found")
        return event