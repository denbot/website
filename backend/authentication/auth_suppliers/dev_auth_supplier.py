from authentication.auth_suppliers.auth_supplier import AuthSupplier
from authentication.enums import AuthStatus


class DevAuthSupplier(AuthSupplier):
    def __init__(
        self,
        phone_ending_attempts: str = "429",
        approve_code: str = "009586",
        failed_code: str = "500500",
        expired_code: str = "000000",
        too_many_attempts_code: str = "429429",
    ) -> None:
        self.phone_ending_attempts = phone_ending_attempts
        self.approve_code = approve_code
        self.failed_code = failed_code
        self.expired_code = expired_code
        self.too_many_attempts_code = too_many_attempts_code

    def send_code(self, phone_number: str) -> AuthStatus:
        if (
            phone_number[-len(self.phone_ending_attempts) :]
            == self.phone_ending_attempts
        ):
            return AuthStatus.TOO_MANY_ATTEMPTS
        return AuthStatus.CREATED

    def verify_code(self, phone_number: str, verification_code: str) -> AuthStatus:
        match verification_code:
            case self.approve_code:
                return AuthStatus.APPROVED
            case self.failed_code:
                return AuthStatus.FAILED
            case self.expired_code:
                return AuthStatus.EXPIRED
            case self.too_many_attempts_code:
                return AuthStatus.TOO_MANY_ATTEMPTS
            case _:
                return AuthStatus.ERROR
