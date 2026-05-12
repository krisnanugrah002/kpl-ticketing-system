from abc import ABC, abstractmethod
from uuid import UUID
from typing import Optional
from src.domain.aggregates.booking import Booking

class BookingRepository(ABC):
    @abstractmethod
    def save(self, booking: Booking) -> None:
        pass

    @abstractmethod
    def get_by_id(self, booking_id: UUID) -> Optional[Booking]:
        pass
    
    @abstractmethod
    def get_active_booking_by_customer_event(self, customer_id: UUID, event_id: UUID) -> Optional[Booking]:
        pass