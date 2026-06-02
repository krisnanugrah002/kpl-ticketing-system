import uuid
from abc import ABC, abstractmethod
from src.application.dtos.sales_report_dto import SalesReportDTO

class SalesQueryService(ABC):
    @abstractmethod
    def get_event_sales_report(self, event_id: uuid.UUID) -> SalesReportDTO:
        pass