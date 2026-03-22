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


class NoConfigurationSuppliedError(AuthImproperlyConfiguredError):
    def __str__(self) -> str:
        return "AUTH_SUPPLIER is not configured"


class NoPathSuppliedError(AuthImproperlyConfiguredError):
    def __str__(self) -> str:
        return "AUTH_SUPPLIER['PATH'] is required"


class BadPathSuppliedError(AuthImproperlyConfiguredError):
    def __init__(self, path: str) -> None:
        self.path = path


class PathDoesNotExistError(BadPathSuppliedError):
    def __str__(self) -> str:
        return "${self.path} is not a valid class path"


class PathIsNotAuthSupplierError(BadPathSuppliedError):
    def __str__(self) -> str:
        return "${self.path} is not an implementation of AuthSupplier"


class InvalidConfigError(AuthImproperlyConfiguredError):
    def __init__(self, classname: str, error: str) -> None:
        self.classname = classname
        self.error = error

    def __str__(self) -> str:
        return "Invalid ${self.classname} config: ${self.error}"
