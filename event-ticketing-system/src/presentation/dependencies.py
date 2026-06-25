from fastapi import Depends
from sqlalchemy.orm import Session

from src.infrastructure.database.session import get_session
from src.infrastructure.repositories.event_repository_impl import EventRepositoryImpl
from src.infrastructure.repositories.ticket_repository_impl import TicketRepositoryImpl
from src.infrastructure.repositories.booking_repository_impl import BookingRepositoryImpl
from src.infrastructure.repositories.refund_repository_impl import RefundRepositoryImpl

from src.infrastructure.services.event_query_service_impl import EventQueryServiceImpl
from src.infrastructure.services.payment_gateway_impl import MockPaymentGatewayImpl
from src.infrastructure.services.sales_query_service_impl import SalesQueryServiceImpl

from src.application.command_handlers.create_event_handler import CreateEventHandler
from src.application.command_handlers.publish_event_handler import PublishEventHandler
from src.application.command_handlers.check_in_handler import CheckInHandler
from src.application.command_handlers.create_booking_handler import CreateBookingHandler
from src.application.command_handlers.pay_booking_handler import PayBookingHandler
from src.application.command_handlers.approve_refund_handler import ApproveRefundHandler

from src.application.query_handlers.get_available_events_handler import GetAvailableEventsHandler
from src.application.query_handlers.get_event_participants_handler import GetEventParticipantsHandler
from src.application.query_handlers.get_event_sales_report_handler import GetEventSalesReportHandler
from src.application.command_handlers.cancel_event_handler import CancelEventHandler

from src.application.command_handlers.disable_ticket_category_handler import DisableTicketCategoryHandler

def get_payment_gateway() -> MockPaymentGatewayImpl:
    return MockPaymentGatewayImpl()

def get_event_repository(session: Session = Depends(get_session)) -> EventRepositoryImpl:
    return EventRepositoryImpl(session)

def get_ticket_repository(session: Session = Depends(get_session)) -> TicketRepositoryImpl:
    return TicketRepositoryImpl(session)

def get_booking_repository(session: Session = Depends(get_session)) -> BookingRepositoryImpl:
    return BookingRepositoryImpl(session)

def get_refund_repository(session: Session = Depends(get_session)) -> RefundRepositoryImpl:
    return RefundRepositoryImpl(session)

def get_event_query_service(session: Session = Depends(get_session)) -> EventQueryServiceImpl:
    return EventQueryServiceImpl(session)

def get_sales_query_service(session: Session = Depends(get_session)) -> SalesQueryServiceImpl:
    return SalesQueryServiceImpl(session)

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

def get_create_booking_handler(
    event_repo = Depends(get_event_repository),
    booking_repo = Depends(get_booking_repository)
) -> CreateBookingHandler:
    return CreateBookingHandler(event_repo, booking_repo)

def get_pay_booking_handler(
    booking_repo = Depends(get_booking_repository),
    ticket_repo = Depends(get_ticket_repository),
    gateway = Depends(get_payment_gateway)
) -> PayBookingHandler:
    return PayBookingHandler(booking_repo, ticket_repo, gateway)

def get_approve_refund_handler(
    refund_repo = Depends(get_refund_repository),
    booking_repo = Depends(get_booking_repository),
    ticket_repo = Depends(get_ticket_repository)
) -> ApproveRefundHandler:
    return ApproveRefundHandler(refund_repo, booking_repo, ticket_repo)

def get_sales_report_handler(
    query_service = Depends(get_sales_query_service)
) -> GetEventSalesReportHandler:
    return GetEventSalesReportHandler(query_service)

def get_disable_ticket_category_handler(repository: EventRepositoryImpl = Depends(get_event_repository)) -> DisableTicketCategoryHandler:
    return DisableTicketCategoryHandler(repository)

def get_cancel_event_handler(repository: EventRepositoryImpl = Depends(get_event_repository)) -> CancelEventHandler:
    return CancelEventHandler(repository)