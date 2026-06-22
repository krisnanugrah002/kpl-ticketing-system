import uuid
from fastapi import APIRouter, Depends, HTTPException

from src.application.queries.get_event_sales_report_query import GetEventSalesReportQuery
from src.application.query_handlers.get_event_sales_report_handler import GetEventSalesReportHandler
from src.presentation.dependencies import get_sales_report_handler

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("/sales")
def get_sales_report(
    event_id: uuid.UUID, 
    handler: GetEventSalesReportHandler = Depends(get_sales_report_handler)
):
    try:
        query = GetEventSalesReportQuery(event_id=event_id)
        report = handler.handle(query)
        return report
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))