import os

from alembic import context
from dotenv import load_dotenv
from sqlalchemy import create_engine

from src.models import Base

load_dotenv()

target_metadata = Base.metadata


def run_migrations() -> None:
    connectable = create_engine(os.environ["DB_URL"])

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


run_migrations()
