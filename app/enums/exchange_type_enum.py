from enum import Enum

class ExchangeType(str, Enum):
    PENDING = "pending_exchange"
    COMPLETED = "exchange_completed"
    CANCELLED = "exchange_cancelled"
    ERROR = "error"