import os
from dotenv import load_dotenv, find_dotenv
from pathlib import Path
from .core import PostgresDB


try:
    env_file = find_dotenv()
    load_dotenv(env_file)
except OSError:
    envp = Path.cwd().parent / ".env"
    load_dotenv(dotenv_path=envp.as_posix())

USER = os.environ.get("POSTGRES_USER")
DB_NAME = os.environ.get("POSTGRES_DATABASE")
PASSWORD = os.environ.get("POSTGRES_PASSWORD")
PORT = os.environ.get("POSTGRES_PORT")
HOST = os.environ.get("POSTGRES_HOST")


def get_db_properties():
    postgres_db = {
        "drivername": "postgresql",
        "username": USER,
        "password": PASSWORD,
        "host": HOST,
        "port": PORT,
        "database": DB_NAME,
    }

    return postgres_db

# connect DB
def get_db():
    db = PostgresDB(get_db_properties(), 'public')

    # return session
    return db.get_session()