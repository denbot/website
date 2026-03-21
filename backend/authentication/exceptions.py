class JWTValidationError(Exception):
    pass


class TokenError(JWTValidationError):
    pass


class UserError(JWTValidationError):
    user_id: str = None

    def __init__(self, id: str) -> None:
        self.user_id = id


class MissingUserIdError(TokenError):
    def __str__() -> str:
        return "Token missing user ID."


class AccountInactiveError(UserError):
    def __str__(self) -> str:
        return "User account inactive. ID: ${self.user_id}."


class TokenExpiredError(TokenError):
    def __str__() -> str:
        return "Token expired."


class InvalidTokenError(TokenError):
    def __str__() -> str:
        return "Token invalid."


class UserDoesNotExistError(UserError):
    def __str__(self) -> str:
        return "User does not exist. ID: ${self.user_id}."


class NoTokenProvidedError(TokenError):
    def __str__() -> str:
        return "No token provided."
