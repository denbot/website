from typing import Protocol, Any

import jwt
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken, T, AuthUser
from rest_framework_simplejwt.utils import datetime_to_epoch

from denbot.jwt.keys import JWTSigningKeys
from denbot.seasons import get_end_of_fiscal_year


class HasPayload(Protocol):
    @property
    def payload(self) -> dict[str, Any]: ...


class KeyIdMintMixin:
    def __str__(self: HasPayload) -> str:
        from django.conf import settings

        keys: JWTSigningKeys = settings.JWT_SIGNING_KEYS

        # Payload is on AccessToken/RefreshToken, not in our mixin
        return jwt.encode(
            self.payload,
            keys.signing_key_pem,
            algorithm="RS256",
            headers={"kid": keys.key_id},
        )


class DenbotAccessToken(KeyIdMintMixin, AccessToken):
    pass


class DenbotRefreshToken(KeyIdMintMixin, RefreshToken):
    access_token_class = (
        DenbotAccessToken  # Spawns CustomAccessToken when calling .access_token
    )

    @classmethod
    def for_user(cls: type[T], user: AuthUser) -> T:
        token = super().for_user(user)

        # Expiring at the end of the fiscal year just means students don't have to worry about logging in again in the
        # middle of the build season.
        token["exp"] = datetime_to_epoch(get_end_of_fiscal_year())

        return token
