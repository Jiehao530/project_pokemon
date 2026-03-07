from enum import Enum

class ExchangeType(str, Enum):
    INCOMING = "incoming_exchange"
    COMPLETED = "exchange_completed"
    CANCELLED = "exchange_cancelled"
    ERROR = "error"