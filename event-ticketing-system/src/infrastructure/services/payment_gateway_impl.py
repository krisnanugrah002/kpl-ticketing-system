import uuid
from src.application.interfaces.payment_gateway import PaymentGateway
from src.domain.value_objects.money import Money

class MockPaymentGatewayImpl(PaymentGateway):
    def process_payment(self, booking_id: uuid.UUID, amount: Money) -> bool:
        print(f"[MOCK PAYMENT] Successfully processed payment of {amount.amount} for booking {booking_id}")
        return True