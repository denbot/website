import os
from datetime import datetime, timedelta, timezone

import jwt
from django.conf import settings
from django.http import HttpRequest
from rest_framework.response import Response
from rest_framework.views import APIView
from twilio.rest import Client

from authentication.utils.validate_jwt import validate_jwt

api_key = os.environ["TWILIO_API_KEY"]
api_secret = os.environ["TWILIO_API_SECRET"]
account_sid = os.environ["TWILIO_ACCOUNT_SID"]
service_sid = os.environ["TWILIO_SERVICE_SID"]
client = Client(api_key, api_secret, account_sid)


class LoginAPIView(APIView):
    def post(self, request: HttpRequest) -> Response:
        phone_number = request.data.get("phoneNumber", "")

        # Send off twilio thing here
        twilio_response = client.verify.v2.services(service_sid).verifications.create(
            to=phone_number, channel="sms"
        )
        return Response({"status": twilio_response.status})


class LoginOtpAPIView(APIView):
    def addJWT(self, response: Response) -> None:
        # for testing, 12345 for id and 1 hour expiry, needs to be updated later.
        # TODO: set these to better values (actual user id and end of the season)
        payload = {
            "user_id": "12345",
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

        # Send off twilio thing here
        twilio_response = client.verify.v2.services(
            service_sid
        ).verification_checks.create(to=phone_number, code=verification_code)

        response = Response({"status": twilio_response.status})

        if twilio_response.status == "approved":
            self.addJWT(response)

        return response


class JWTVerificationView(APIView):
    def get(self, request: HttpRequest) -> Response:
        token = request.COOKIES.get("authToken")
        try:
            payload = validate_jwt(token)
            return Response({"valid": True, "user_id": payload.get("user_id")})
        except ValueError as e:
            return Response({"valid": False, "reason": str(e)}, status=401)
