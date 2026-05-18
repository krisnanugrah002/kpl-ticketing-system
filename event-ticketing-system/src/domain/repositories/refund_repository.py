import uuid
from abc import ABC, abstractmethod
from typing import Optional
from src.domain.aggregates.refund import Refund

class RefundRepository(ABC):
    
    @abstractmethod
    def save(self, refund: Refund) -> None:
        """Menyimpan atau memperbarui data Aggregate Refund."""
        pass
        
    @abstractmethod
    def get_by_id(self, refund_id: uuid.UUID) -> Optional[Refund]:
        """Mengambil data Refund berdasarkan ID."""
        pass

    @abstractmethod
    def get_by_booking_id(self, booking_id: uuid.UUID) -> Optional[Refund]:
        """Mengambil data Refund berdasarkan Booking ID untuk mengecek duplikasi."""
        pass