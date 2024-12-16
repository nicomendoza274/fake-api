from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from core.classes.settings import settings

DATABASE_URI = settings.DB_URI

engine = create_engine(DATABASE_URI)


# Dependency
def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
