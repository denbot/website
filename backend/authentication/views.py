from django.http import HttpRequest
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.utils import datetime_from_epoch

from authentication.enums import AuthStatus
from authentication.exceptions import JWTValidationError
from authentication.models import DenbotUser
from authentication.utils.auth import get_auth_supplier
from authentication.utils.validate_jwt import validate_jwt
from denbot.jwt.tokens import DenbotRefreshToken


class LoginAPIView(APIView):
    def post(self, request: HttpRequest) -> Response:
        phone_number = request.data.get("phoneNumber", "")
        # don't create user here, wait until they have verified.
        status = get_auth_supplier().send_code(phone_number)
        if status != AuthStatus.ERROR:
            return Response({"status": status})
        else:
            return Response({"status": status}, status=500)


class LoginOtpAPIView(APIView):
    @staticmethod
    def add_jwt(user: DenbotUser, response: Response) -> None:
        refresh_token: DenbotRefreshToken = DenbotRefreshToken.for_user(user)

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="Lax",
            path="/api/token/refresh",
            expires=datetime_from_epoch(refresh_token["exp"]),
        )

        access_token = refresh_token.access_token
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
            samesite="Lax",
            expires=datetime_from_epoch(access_token["exp"]),
        )

    def post(self, request: HttpRequest) -> Response:
        phone_number = request.data.get("phoneNumber", "")
        verification_code = request.data.get("verificationCode", "")
        status = get_auth_supplier().verify_code(phone_number, verification_code)

        response = Response({"status": status})

        if status == AuthStatus.ERROR:
            response.status_code = 500
        if status == AuthStatus.APPROVED:
            # TODO: Don't create user here, should be a separate path for that
            user = DenbotUser.objects.get_or_create_user(phone=phone_number)
            self.add_jwt(user, response)

        return response


class JWTVerificationView(APIView):
    def get(self, request: HttpRequest) -> Response:
        token = request.COOKIES.get("auth_token")
        try:
            payload = validate_jwt(token)
            return Response({"valid": True, "user_id": payload.get("user_id")})
        except JWTValidationError as e:
            return Response({"valid": False, "reason": str(e)}, status=401)
