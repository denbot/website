from dataclasses import dataclass

from authentication.auth_suppliers.auth_supplier import AuthSupplier
from authentication.enums import AuthStatus
from authentication.exceptions import InvalidConfigError


@dataclass(frozen=True)
class DevAuthConfig:
    phone_ending_attempts: str = "429"
    approve_code: str = "009586"
    error_code: str = "500500"
    expired_code: str = "000000"
    too_many_attempts_code: str = "429429"


class DevAuthSupplier(AuthSupplier):
    def __init__(self, config: DevAuthConfig) -> None:
        self._phone_ending_attempts = config.phone_ending_attempts
        self._approve_code = config.approve_code
        self._error_code = config.error_code
        self._expired_code = config.expired_code
        self._too_many_attempts_code = config.too_many_attempts_code

    @classmethod
    def from_settings(cls, options: dict) -> "DevAuthSupplier":
        try:
            config = DevAuthConfig(**options)
        except TypeError as e:
            raise InvalidConfigError(cls.__name__, e)

        return cls(config)

    def send_code(self, phone_number: str) -> AuthStatus:
        if phone_number.endswith(self._phone_ending_attempts):
            return AuthStatus.TOO_MANY_ATTEMPTS
        return AuthStatus.CREATED

    def verify_code(self, phone_number: str, verification_code: str) -> AuthStatus:
        match verification_code:
            case self._approve_code:
                return AuthStatus.APPROVED
            case self._error_code:
                return AuthStatus.ERROR
            case self._expired_code:
                return AuthStatus.EXPIRED
            case self._too_many_attempts_code:
                return AuthStatus.TOO_MANY_ATTEMPTS
            case _:
                return AuthStatus.FAILED
