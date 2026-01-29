class JWTValidationError(Exception):
    pass


class TokenError(JWTValidationError):
    pass


class UserError(JWTValidationError):
    pass


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
