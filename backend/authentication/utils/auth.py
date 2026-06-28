from django.conf import settings
from django.utils.module_loading import import_string

from authentication.auth_suppliers.auth_supplier import AuthSupplier
from authentication.exceptions import (
    AuthSupplierUnspecifiedError,
    BackendDoesNotExistError,
    BackendIsNotAuthSupplierError,
    NoBackendSuppliedError,
)


def get_auth_supplier() -> AuthSupplier:
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
