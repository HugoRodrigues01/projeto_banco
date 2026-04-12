from sqlalchemy import create_engine
from src.settings import Settings
from src.models.users import table_registry

engine = create_engine(Settings().DATABASE_URL)
table_registry.metadata.create_all(engine)