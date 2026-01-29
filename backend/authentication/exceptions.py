class JWTValidationError(Exception):
    pass


class TokenError(JWTValidationError):
    pass


class UserError(JWTValidationError):
    user_id: str = None

    def __init__(self, id: str) -> None:
        self.user_id = id


class MissingUserIdError(TokenError):
    pass


class AccountInactiveError(UserError):
    pass


class TokenExpiredError(TokenError):
    pass


class InvalidTokenError(TokenError):
    pass


class UserDoesNotExistError(UserError):
    pass


class NoTokenProvidedError(TokenError):
    pass
