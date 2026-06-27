from django.contrib.auth.backends import BaseBackend
from django.http import HttpRequest

from authentication.enums import AuthStatus
from authentication.exceptions import OtpAuthError
from authentication.models import DenbotUser
from authentication.utils.auth import get_auth_supplier


class OTPBackend(BaseBackend):
    def authenticate(
        self, request: HttpRequest, phone_number: str = None, otp: str = None
    ) -> DenbotUser:
        status = get_auth_supplier().verify_code(phone_number, otp)

        if status == AuthStatus.APPROVED:
            try:
                user = DenbotUser.objects.get(phone=phone_number)
                return user
            except DenbotUser.DoesNotExist:
                return None

        raise OtpAuthError(status)

    def get_user(self, phone_number: str) -> DenbotUser:
        try:
            return DenbotUser.objects.get(phone_number=phone_number)
        except DenbotUser.DoesNotExist:
            return None
