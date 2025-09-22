from datetime import datetime, timezone

import jwt
from django.conf import settings


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

        return payload

    except jwt.ExpiredSignatureError:
        raise ValueError("Token expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")
