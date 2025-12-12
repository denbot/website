from datetime import datetime, timezone

import jwt
from django.conf import settings

from authentication.models import DenbotUser


def validate_jwt(token: str) -> dict:
    """Return payload if valid, else raise exception"""
    if not token:
        raise ValueError("No token provided")

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        exp = payload.get("exp")
        if exp is None:
            raise ValueError("Token missing expiration")

        if datetime.now(timezone.utc).timestamp() > exp:
            raise ValueError("Token expired")

        id = payload.get("user_id")
        if id is None:
            raise ValueError("Token missing user id")

        user = DenbotUser.objects.get(id=id)
        if not user.is_active:
            raise ValueError("User account not active")

        return payload

    except jwt.ExpiredSignatureError:
        raise ValueError("Token expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")
    except DenbotUser.DoesNotExist:
        raise ValueError("User Does Not Exist")
