import os
from sqlalchemy import create_engine


DATABASE_URL = os.environ.get(
    "DATABASE_URL", 
    "postgresql://postgres:akuvalen@localhost:5432/event_ticketing_db" #Ini disesuain sama Pass Postgress sendiri ya kris
)

engine = create_engine(DATABASE_URL, echo=True)