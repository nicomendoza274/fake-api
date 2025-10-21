from contextlib import contextmanager
from typing import Generator

from sqlalchemy.orm import Session
from sqlmodel import Session as SQLModelSession

from core.database.database import engine


class TransactionManager:
    """Manager to handle database transactions"""

    @staticmethod
    @contextmanager
    def get_transaction() -> Generator[Session, None, None]:
        """Context manager for synchronous transactions"""
        session = SQLModelSession(engine)
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    @staticmethod
    def execute_in_transaction(func, *args, **kwargs):
        """Execute a function within a transaction"""
        with TransactionManager.get_transaction() as session:
            return func(session, *args, **kwargs)


class DatabaseTransaction:
    """Decorator to automatically handle transactions"""

    def __init__(self, auto_commit: bool = True):
        self.auto_commit = auto_commit

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            # Search for the session in the arguments
            session = None
            for arg in args:
                if isinstance(arg, Session):
                    session = arg
                    break

            if not session:
                # If there is no session, create a new transaction
                with TransactionManager.get_transaction() as new_session:
                    # Replace the first argument with the new session
                    if args and hasattr(args[0], "session"):
                        args[0].session = new_session
                    return func(*args, **kwargs)
            else:
                # If there is a session, use the normal function
                return func(*args, **kwargs)

        return wrapper


# Convenience decorator
def with_transaction(auto_commit: bool = True):
    """Decorator to automatically handle transactions"""
    return DatabaseTransaction(auto_commit=auto_commit)


# Context manager for nested transactions
@contextmanager
def nested_transaction(session: Session):
    """Create a nested transaction (savepoint)"""
    savepoint = session.begin_nested()
    try:
        yield session
        savepoint.commit()
    except Exception:
        savepoint.rollback()
        raise
