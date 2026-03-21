import jwt
from django.conf import settings

import authentication.exceptions as jwtExceptions
from authentication.models import DenbotUser


def validate_jwt(token: str) -> dict:
    """Return payload if valid, else raise exception"""
    if not token:
        raise jwtExceptions.NoTokenProvidedError

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

        id = payload.get("user_id")
        if id is None:
            raise jwtExceptions.MissingUserIdError

        user = DenbotUser.objects.get(id=id)
        if not user.is_active:
            raise jwtExceptions.AccountInactiveError(id)

        return payload

    except jwt.ExpiredSignatureError:
        raise jwtExceptions.TokenExpiredError
    except jwt.InvalidTokenError:
        raise jwtExceptions.InvalidTokenError
    except DenbotUser.DoesNotExist:
        raise jwtExceptions.UserDoesNotExistError(id)
