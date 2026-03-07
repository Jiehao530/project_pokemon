from enum import Enum

class ActionsExchange(str, Enum):
    REQUEST = "request"
    ACCEPT = "accept"
    CANCEL = "cancel"