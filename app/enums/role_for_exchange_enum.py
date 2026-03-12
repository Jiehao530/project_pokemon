from enum import Enum

class ExchangeRole(str, Enum):
    CREATOR = "creator"
    PARTICIPANT = "participant"