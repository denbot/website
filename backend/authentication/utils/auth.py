from django.conf import settings
from django.utils.module_loading import import_string

from authentication.auth_suppliers.auth_supplier import AuthSupplier
from authentication.enums import AuthStatus
from authentication.exceptions import (
    AuthSupplierUnspecifiedError,
    NoBackendSuppliedError,
    BackendDoesNotExistError,
    BackendIsNotAuthSupplierError,
)


class Auth:
    _supplier: AuthSupplier = None

    @classmethod
    def _get_auth(cls) -> AuthSupplier:
        if cls._supplier is not None:
            return cls._supplier

        config = getattr(settings, "AUTH_SUPPLIER", None)

        if not config:
            raise AuthSupplierUnspecifiedError

        backend_path = config.get("BACKEND")
        options = config.get("OPTIONS", {})

        if not backend_path:
            raise NoBackendSuppliedError

        try:
            cls = import_string(backend_path)
        except ImportError:
            raise BackendDoesNotExistError(backend_path)

        if not issubclass(cls, AuthSupplier):
            raise BackendIsNotAuthSupplierError(backend_path)

        return cls.from_settings(options)

    @classmethod
    def send_code(self, phone_number: str) -> AuthStatus:
        return self._get_auth().send_code(phone_number)

    @classmethod
    def verify_code(self, phone_number: str, verification_code: str) -> AuthStatus:
        return self._get_auth().verify_code(phone_number, verification_code)
