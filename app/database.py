import os
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


def get_database_url() -> str:
    password_file = os.getenv("DB_PASSWORD_FILE")
    if password_file and Path(password_file).exists():
        db_password = Path(password_file).read_text(encoding="utf-8").strip()
    else:
        db_password = os.getenv("POSTGRES_PASSWORD", "taskflow123")

    db_user = os.getenv("POSTGRES_USER", "taskflow")
    db_name = os.getenv("POSTGRES_DB", "taskflow_db")
    db_host = os.getenv("POSTGRES_HOST", "db")
    db_port = os.getenv("POSTGRES_PORT", "5432")

    return os.getenv(
        "DATABASE_URL",
        f"postgresql+psycopg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}",
    )


DATABASE_URL = get_database_url()

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()