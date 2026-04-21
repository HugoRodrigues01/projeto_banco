from src.models import accounts, banks, transactions, users
from src.models.registry import table_registry

metadata = table_registry.metadata

__all__ = ["users", "banks", "accounts", "transactions"]
