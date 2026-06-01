import uuid
from abc import ABC, abstractmethod
from src.domain.value_objects.money import Money

class PaymentGateway(ABC):
    @abstractmethod
    def process_payment(self, booking_id: uuid.UUID, amount: Money) -> bool:
        """
        Next : Implementasi pembayaran ke third party gateway pada layer infrastructure.
        """
        pass