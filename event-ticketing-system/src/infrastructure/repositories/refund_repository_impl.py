import uuid
from typing import Optional
from sqlalchemy.orm import Session
from src.domain.repositories.refund_repository import RefundRepository
from src.domain.aggregates.refund import Refund, RefundStatus
from src.domain.value_objects.money import Money
from src.infrastructure.database.models.refund_model import RefundModel

class RefundRepositoryImpl(RefundRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, refund: Refund) -> None:
        model = self.session.query(RefundModel).filter_by(id=refund.id).first()
        if not model:
            model = RefundModel(id=refund.id)
            self.session.add(model)

        model.booking_id = refund.booking_id
        model.amount = refund.amount.amount
        model.status = refund.status.value
        model.rejection_reason = refund.rejection_reason
        model.payment_reference = refund.payment_reference
        self.session.commit()

    def get_by_id(self, refund_id: uuid.UUID) -> Optional[Refund]:
        model = self.session.query(RefundModel).filter_by(id=refund_id).first()
        if not model:
            return None

        refund = Refund(
            id=model.id,
            booking_id=model.booking_id,
            amount=Money(model.amount),
            status=RefundStatus(model.status),
            rejection_reason=model.rejection_reason or "",
            payment_reference=model.payment_reference or ""
        )
        return refund

    def get_by_booking_id(self, booking_id: uuid.UUID) -> Optional[Refund]:
        model = self.session.query(RefundModel).filter_by(booking_id=booking_id).first()
        return self.get_by_id(model.id) if model else None