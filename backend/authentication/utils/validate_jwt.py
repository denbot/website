import exceptions
import jwt
from django.conf import settings

from authentication.models import DenbotUser


def validate_jwt(token: str) -> dict:
    """Return payload if valid, else raise exception"""
    if not token:
        raise exceptions.NoTokenProvidedError

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

        id = payload.get("user_id")
        if id is None:
            raise exceptions.MissingUserIdError

        user = DenbotUser.objects.get(id=id)
        if not user.is_active:
            raise exceptions.AccountInactiveError

        return payload

    except jwt.ExpiredSignatureError:
        raise exceptions.TokenExpiredError
    except jwt.InvalidTokenError:
        raise exceptions.InvalidTokenError
    except DenbotUser.DoesNotExist:
        raise exceptions.UserDoesNotExistError
