from src.models import banks, users, acounts
from src.models.registry import table_registry

metadata = table_registry.metadata

__all__ = ["users", "banks", "acounts"]
