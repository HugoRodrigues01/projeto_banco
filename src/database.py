from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.models.users import table_registry
from src.settings import Settings

engine = create_engine(Settings().DATABASE_URL)
table_registry.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:  # pragma: no cover
        yield session
