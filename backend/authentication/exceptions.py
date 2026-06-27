from django.core.exceptions import PermissionDenied

from authentication.enums import AuthStatus


class JWTValidationError(Exception):
    pass


class TokenError(JWTValidationError):
    pass


class UserError(JWTValidationError):
    def __init__(self, id: str) -> None:
        self.user_id = id


class MissingUserIdError(TokenError):
    def __str__(self) -> str:
        return "Token missing user ID."


class AccountInactiveError(UserError):
    def __str__(self) -> str:
        return "User account inactive. ID: ${self.user_id}."


class TokenExpiredError(TokenError):
    def __str__(self) -> str:
        return "Token expired."


class InvalidTokenError(TokenError):
    def __str__(self) -> str:
        return "Token invalid."


class UserDoesNotExistError(UserError):
    def __str__(self) -> str:
        return "User does not exist. ID: ${self.user_id}."


class NoTokenProvidedError(TokenError):
    def __str__(self) -> str:
        return "No token provided."


class AuthImproperlyConfiguredError(Exception):
    pass


class AuthSupplierUnspecifiedError(AuthImproperlyConfiguredError):
    def __str__(self) -> str:
        return "AUTH_SUPPLIER is not configured in the settings"


class NoBackendSuppliedError(AuthImproperlyConfiguredError):
    def __str__(self) -> str:
        return "AUTH_SUPPLIER['BACKEND'] is required"


class BadBackendSuppliedError(AuthImproperlyConfiguredError):
    def __init__(self, backend: str) -> None:
        self.backend = backend


class BackendDoesNotExistError(BadBackendSuppliedError):
    def __str__(self) -> str:
        return "${self.backend} is not a valid class path"


class BackendIsNotAuthSupplierError(BadBackendSuppliedError):
    def __str__(self) -> str:
        return "${self.backend} is not an implementation of AuthSupplier"


class InvalidConfigError(AuthImproperlyConfiguredError):
    def __init__(self, classname: str, error: str) -> None:
        self.classname = classname
        self.error = error

    def __str__(self) -> str:
        return "Invalid ${self.classname} config: ${self.error}"


class OtpAuthError(PermissionDenied):
    def __init__(self, status: AuthStatus) -> None:
        self.status = status
