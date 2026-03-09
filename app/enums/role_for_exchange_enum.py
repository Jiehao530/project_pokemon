from enum import Enum

class ExchangeRole(str, Enum):
    CREATOR = "creator"
    PATICIPANT = "participant"