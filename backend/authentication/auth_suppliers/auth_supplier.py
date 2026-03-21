from abc import ABC, abstractmethod

from authentication.enums import AuthStatus


class AuthSupplier(ABC):
    @abstractmethod
    def send_code(self, phone_number: str) -> AuthStatus:
        pass

    @abstractmethod
    def verify_code(self, phone_number: str, verification_code: str) -> AuthStatus:
        pass
