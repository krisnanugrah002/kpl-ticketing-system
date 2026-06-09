from fastapi import FastAPI

app = FastAPI(title="Event Ticketing System API")

@app.get("/")
def read_root():
    return {"status": "API is running"}