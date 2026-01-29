from enum import Enum


class AuthStatus(Enum):
    APPROVED = "approved"
    CREATED = "created"
    ERROR = "error"
    EXPIRED = "expired"
    FAILED = "failed"
    TOO_MANY_ATTEMPTS = "too_many_attempts"
