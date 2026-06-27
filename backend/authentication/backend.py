from django.contrib.auth.backends import BaseBackend
from django.http import HttpRequest

from authentication.enums import AuthStatus
from authentication.models import DenbotUser
from authentication.utils.auth import get_auth_supplier


class OTPBackend(BaseBackend):
    def authenticate(
        self, request: HttpRequest, username: str = None, password: str = None
    ) -> DenbotUser:
        status = get_auth_supplier().verify_code(username, password)

        if status == AuthStatus.APPROVED:
            try:
                return DenbotUser.objects.get(phone=username)
            except DenbotUser.DoesNotExist:
                return None
        return None

    def get_user(self, user_id: str) -> DenbotUser:
        try:
            return DenbotUser.objects.get(pk=user_id)
        except DenbotUser.DoesNotExist:
            return None
