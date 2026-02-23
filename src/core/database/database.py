from typing import Annotated

from fastapi import Depends
from sqlalchemy.pool import QueuePool
from sqlmodel import Session, create_engine

from src.core.classes.settings import settings

DATABASE_URI = f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

# Advanced engine configuration with connection pooling
engine = create_engine(
    DATABASE_URI,
    # Connection Pooling
    poolclass=QueuePool,
    pool_size=20,  # Number of persistent connections
    max_overflow=30,  # Additional connections when the pool is exhausted
    pool_pre_ping=True,  # Check connections before using
    pool_recycle=3600,  # Recycle connections every hour
    # Performance
    echo=settings.DEBUG,  # Log SQL queries in debug mode
    echo_pool=settings.DEBUG,  # Log pool events in debug mode
    # Connection timeout
    connect_args={
        "connect_timeout": 10,
        "application_name": "fake_api",
        # "options": "-c default_transaction_isolation='read committed'",
    },
)


def get_session():
    """Dependency to get a database session"""
    with Session(engine) as session:
        try:
            yield session
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()


SessionDep = Annotated[Session, Depends(get_session)]
