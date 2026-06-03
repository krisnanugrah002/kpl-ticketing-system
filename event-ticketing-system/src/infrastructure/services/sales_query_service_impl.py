import uuid
from sqlalchemy.orm import Session
from src.application.interfaces.sales_query_service import SalesQueryService
from src.application.dtos.sales_report_dto import SalesReportDTO
from src.infrastructure.database.models.booking_model import BookingModel

class SalesQueryServiceImpl(SalesQueryService):
    def __init__(self, session: Session):
        self.session = session

    def get_event_sales_report(self, event_id: uuid.UUID) -> SalesReportDTO:
        bookings = self.session.query(BookingModel).filter_by(event_id=event_id).all()

        paid_bookings = [b for b in bookings if b.status == "Paid"]
        total_revenue = sum(b.total_price for b in paid_bookings)

        return SalesReportDTO(
            event_id=event_id,
            tickets_sold_per_category={},
            total_pending_bookings=len([b for b in bookings if b.status == "PendingPayment"]),
            total_paid_bookings=len(paid_bookings),
            total_expired_bookings=len([b for b in bookings if b.status == "Expired"]),
            total_refunded_bookings=len([b for b in bookings if b.status == "Refunded"]),
            total_revenue=float(total_revenue)
        )