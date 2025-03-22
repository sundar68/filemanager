from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import text
from db import session as db_session
from .base import Base

class PostgresIntegration:
    def __init__(self):
        self.engine = db_session._ASYNC_ENGINE
        self._Base = Base

    def get_postgres_conn(self):
        """
        Get a new database session.
        """
        return db_session.get_async_session()

    def get_postgres_base(self):
        """
        Get the declarative base for model definition.
        """
        return self._Base

    def check_postgres_connection(self):
        """
        Check if the connection to the PostgreSQL database is successful.
        """
        try:
            with self.engine.connect() as conn:
                result = conn.execute("SELECT 1")  # Test query to check connection
                return result.fetchone() is not None
        except SQLAlchemyError as err:
            raise Exception(f"Error while connecting to PostgreSQL: {err}")

    def execute_custom_read_query(self, query: str, db: Session):
        """
        Execute a custom read-only query on the PostgreSQL database.
        The session is passed from the FastAPI route handler.
        """
        try:
            return list(db.execute(text(query)))
        except SQLAlchemyError as err:
            raise Exception(f"Error while executing custom PostgreSQL Query: {err}")
