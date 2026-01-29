from django.conf import settings
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client


class TwilioAuth:
    def __init__(self) -> None:
        self.api_key = settings.TWILIO_API_KEY
        self.api_secret = settings.TWILIO_API_SECRET
        self.account_sid = settings.TWILIO_ACCOUNT_SID
        self.service_sid = settings.TWILIO_SERVICE_SID
        self.client = Client(self.api_key, self.api_secret, self.account_sid)

    def send_code(self, phone_number: str) -> str:
        try:
            twilio_response = self.client.verify.v2.services(
                self.service_sid
            ).verifications.create(to=phone_number, channel="sms")
            if twilio_response.status == "pending":
                return "created"

        except TwilioRestException as error:
            if error.status == 429:
                return "too_many_attempts"

        return "error"

    def verify_code(self, phone_number: str, verification_code: str) -> str:
        try:
            twilio_response = self.client.verify.v2.services(
                self.service_sid
            ).verification_checks.create(to=phone_number, code=verification_code)

            match twilio_response.status:
                case "approved":
                    return "approved"
                case "pending":
                    return "failed"
                case "max_attempts_reached":
                    self.try_twilio_auth_create(phone_number)
                    return "expired"
                case "expired":
                    self.try_twilio_auth_create(phone_number)
                    return "expired"

        except TwilioRestException as error:
            if error.status == 429:
                return "too_many_attempts"

        return "error"
