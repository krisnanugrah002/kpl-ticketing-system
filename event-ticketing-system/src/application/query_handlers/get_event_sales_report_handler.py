from src.application.queries.get_event_sales_report_query import GetEventSalesReportQuery
from src.application.dtos.sales_report_dto import SalesReportDTO
from src.application.interfaces.sales_query_service import SalesQueryService

class GetEventSalesReportHandler:
    def __init__(self, query_service: SalesQueryService):
        self.query_service = query_service

    def handle(self, query: GetEventSalesReportQuery) -> SalesReportDTO:
        return self.query_service.get_event_sales_report(query.event_id)