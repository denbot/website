from django.conf import settings
from django.http import JsonResponse

from denbot.jwt.keys import JWTSigningKeys


def jwks_json(request):
    keys: JWTSigningKeys = settings.JWT_SIGNING_KEYS

    return JsonResponse(keys.jwks)
