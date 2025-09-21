from rest_framework.views import APIView
from rest_framework.response import Response

import os
from twilio.rest import Client

api_key = os.environ["TWILIO_API_KEY"]
api_secret = os.environ["TWILIO_API_SECRET"]
account_sid = os.environ["TWILIO_ACCOUNT_SID"]
service_sid = os.environ['TWILIO_SERVICE_SID']
client = Client(api_key, api_secret, account_sid)


class LoginAPIView(APIView):
    def post(self, request):
        # Probably a better way to get/validate things but I don't know or care what that is rn
        phone_number = request.data.get("phoneNumber", "")

        # Send off twilio thing here
        success = client.verify.v2.services(
            service_sid
        ).verifications.create(to=phone_number, channel="sms")
        return Response({"success": success.status == "pending"})


class LoginOtpAPIView(APIView):
    def post(self, request):
        # Probably a better way to get/validate things but I don't know or care what that is rn
        phone_number = request.data.get("phoneNumber", "")
        verification_code = request.data.get("verificationCode", "")

        # Send off twilio thing here
        success = client.verify.v2.services(
    service_sid
).verification_checks.create(to=phone_number, code=verification_code)
        return Response({"success": success.status == "approved"})