from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker
from loguru import logger


class PostgresDB:
    _instance = None

    def __new__(cls, pg_creds: dict, postgres_schema: str, *args, **kwargs):
        """Singleton constructor for PostgresDB"""
        if cls._instance is None:
            cls._instance = super(PostgresDB, cls).__new__(cls)
            try:
                # Create engine with PostgreSQL credentials
                cls._instance._engine = create_engine(
                    URL.create(**pg_creds),
                    connect_args={"options": f"-csearch_path={postgres_schema}"}
                )
                cls._instance._Session = sessionmaker(bind=cls._instance._engine)
                cls._instance.schema = postgres_schema

                logger.info(f"Connected to {pg_creds.get('database')} at schema {postgres_schema}")
            except Exception as e:
                logger.error(f"Error connecting to PostgresDB: {e}")
                cls._instance = None  # Reset instance on error

        return cls._instance

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def get_connection(self):
        """Establish database connection"""
        return self._engine.connect()

    def get_session(self):
        """Create a new SQLAlchemy session"""
        return self._Session()

    def close(self):
        """Dispose database engine"""
        if self._engine:
            self._engine.dispose()  # close out all connections
            logger.info("Close all connections associated with the engine.")
