from fastapi import FastAPI
from src.presentation.api import events, tickets, bookings, refunds, reports

app = FastAPI(title="Event Ticketing System API")

app.include_router(events.router)
app.include_router(tickets.router)
app.include_router(bookings.router)
app.include_router(refunds.router)
app.include_router(reports.router)

@app.get("/")
def read_root():
    return {"status": "API is running"}