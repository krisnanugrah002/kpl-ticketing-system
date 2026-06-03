import uuid
from src.application.interfaces.notification_service import NotificationService

class MockNotificationServiceImpl(NotificationService):
    def send_booking_confirmation(self, customer_id: uuid.UUID, booking_id: uuid.UUID) -> None:
        print(f"[MOCK EMAIL] Booking confirmation sent to customer {customer_id} for booking {booking_id}")

    def send_ticket_issued_alert(self, customer_id: uuid.UUID, tickets: list) -> None:
        print(f"[MOCK EMAIL] E-Tickets sent to customer {customer_id}. Total tickets: {len(tickets)}")