from datetime import datetime, timedelta, timezone

import jwt
from django.conf import settings
from django.http import HttpRequest
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.enums import AuthStatus
from authentication.exceptions import JWTValidationError
from authentication.models import DenbotUser
from authentication.utils.auth import get_auth_supplier
from authentication.utils.validate_jwt import validate_jwt


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
    def addJWT(self, user: DenbotUser, response: Response) -> None:
        # for testing, 1 hour expiry, needs to be updated later.
        # TODO: set end of the season

        payload = {
            "user_id": str(user.id),
            "exp": datetime.now(timezone.utc) + timedelta(hours=1),
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

        response.set_cookie(
            key="authToken",
            value=token,
            httponly=True,
            secure=True,
            samesite="Lax",
            max_age=3600,
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
            self.addJWT(user, response)

        return response


class JWTVerificationView(APIView):
    def get(self, request: HttpRequest) -> Response:
        token = request.COOKIES.get("authToken")
        try:
            payload = validate_jwt(token)
            return Response({"valid": True, "user_id": payload.get("user_id")})
        except JWTValidationError as e:
            return Response({"valid": False, "reason": str(e)}, status=401)
