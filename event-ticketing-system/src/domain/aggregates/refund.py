import uuid
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
from typing import List
from src.domain.aggregates.booking import Booking, BookingStatus
from src.domain.aggregates.ticket import Ticket, TicketStatus
from src.domain.value_objects.money import Money
from src.domain.events.refund_events import RefundRequested, RefundApproved, RefundRejected, RefundPaidOut

class RefundStatus(Enum):
    REQUESTED = "Requested"
    APPROVED = "Approved"
    REJECTED = "Rejected"
    PAID_OUT = "PaidOut"

@dataclass
class Refund:
    id: uuid.UUID
    booking_id: uuid.UUID
    amount: Money
    status: RefundStatus = field(default=RefundStatus.REQUESTED)
    rejection_reason: str = field(default="")
    payment_reference: str = field(default="")
    domain_events: list = field(default_factory=list)

    @classmethod
    def create(
        cls,
        booking: Booking,
        associated_tickets: List[Ticket],
        refund_deadline: datetime,
        current_time: datetime
    ) -> "Refund":
       
        # BR38:
        if booking.status != BookingStatus.PAID:
            raise ValueError("Refund can only be requested for a Paid booking.")

        # BR39
        if any(ticket.status == TicketStatus.CHECKED_IN for ticket in associated_tickets):
            raise ValueError("Cannot request a refund if any associated ticket has already been checked in.")

        # BR40
        if current_time > refund_deadline:
            raise ValueError("Refund request has passed the allowed deadline.")

        refund = cls(
            id=uuid.uuid4(),
            booking_id=booking.id,
            amount=booking.total_price,
            status=RefundStatus.REQUESTED
        )
        refund.domain_events.append(RefundRequested(refund.id, booking.id))
        return refund

    def approve(self):
        """Logika BR41: Menyetujui pengajuan refund"""
        if self.status != RefundStatus.REQUESTED:
            raise ValueError("Only a requested refund can be approved.")
        
        self.status = RefundStatus.APPROVED
        self.domain_events.append(RefundApproved(self.id))

    def reject(self, reason: str):
        """Logika BR44 & BR45: Menolak pengajuan refund wajib dengan alasan"""
        if self.status != RefundStatus.REQUESTED:
            raise ValueError("Only a requested refund can be rejected.")
        
        if not reason or reason.strip() == "":
            raise ValueError("A rejection reason must be provided.")

        self.status = RefundStatus.REJECTED
        self.rejection_reason = reason
        self.domain_events.append(RefundRejected(self.id, reason))

    def mark_as_paid_out(self, payment_reference: str):
        """Logika BR47, BR48 & BR49: Menandai dana telah ditransfer balik ke customer"""
        if self.status != RefundStatus.APPROVED:
            raise ValueError("Refund must be approved before it can be marked as paid out.")
        
        if not payment_reference or payment_reference.strip() == "":
            raise ValueError("Payment reference code must be provided.")

        self.status = RefundStatus.PAID_OUT
        self.payment_reference = payment_reference
        self.domain_events.append(RefundPaidOut(self.id, payment_reference))