import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

# Named DB_URL, not DATABASE_URL, on purpose:
# the ADK dev tools use DATABASE_URL for their own chat storage.
connection_string = os.getenv("DB_URL")

if not connection_string:
    raise RuntimeError("DB_URL is missing. Add it to your .env file.")

engine = create_engine(connection_string)

db = sessionmaker(bind=engine)
