import os
from sqlmodel import create_engine, SQLModel, Session

# Get the database URL from the environment variable set in docker-compose.yml
DATABASE_URL = os.environ.get("DATABASE_URL")

# The connect_args is needed for SQLite, but not for PostgreSQL.
# However, keeping it here with a check makes the code adaptable.
# For PostgreSQL, it's not needed.
connect_args = {}
# if "sqlite" in DATABASE_URL:
#     connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, echo=True, connect_args=connect_args)

def create_db_and_tables():
    # This is where the magic happens!
    # SQLModel.metadata.create_all() will create all tables that inherit from SQLModel.
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
