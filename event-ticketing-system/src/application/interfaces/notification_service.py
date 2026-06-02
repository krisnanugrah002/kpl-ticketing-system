import uuid
from abc import ABC, abstractmethod

class NotificationService(ABC):
    @abstractmethod
    def send_booking_confirmation(self, customer_id: uuid.UUID, booking_id: uuid.UUID) -> None:
        pass

    @abstractmethod
    def send_ticket_issued_alert(self, customer_id: uuid.UUID, tickets: list) -> None:
        pass