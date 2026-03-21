from enum import Enum

from django.conf import settings
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

from authentication.enums import AuthStatus


class TwilioResponse(Enum):
    APPROVED = "approved"
    CANCELED = "canceled"
    DELETED = "deleted"
    FAILED = "failed"
    EXPIRED = "expired"
    MAX_ATTEMPTS_REACHED = "max_attempts_reached"
    PENDING = "pending"


class TwilioAuth:
    def __init__(self) -> None:
        self.api_key = settings.TWILIO_API_KEY
        self.api_secret = settings.TWILIO_API_SECRET
        self.account_sid = settings.TWILIO_ACCOUNT_SID
        self.service_sid = settings.TWILIO_SERVICE_SID
        self.client = Client(self.api_key, self.api_secret, self.account_sid)

    def send_code(self, phone_number: str) -> AuthStatus:
        try:
            twilio_response = self.client.verify.v2.services(
                self.service_sid
            ).verifications.create(to=phone_number, channel="sms")
            if twilio_response.status == TwilioResponse.PENDING:
                return AuthStatus.CREATED

        except TwilioRestException as error:
            if error.status == 429:
                return AuthStatus.TOO_MANY_ATTEMPTS

        return AuthStatus.ERROR

    def verify_code(self, phone_number: str, verification_code: str) -> AuthStatus:
        try:
            twilio_response = self.client.verify.v2.services(
                self.service_sid
            ).verification_checks.create(to=phone_number, code=verification_code)

            match twilio_response.status:
                case TwilioResponse.APPROVED:
                    return AuthStatus.APPROVED
                case TwilioResponse.PENDING:
                    return AuthStatus.FAILED
                case TwilioResponse.MAX_ATTEMPTS_REACHED:
                    self.try_twilio_auth_create(phone_number)
                    return AuthStatus.EXPIRED
                case TwilioResponse.EXPIRED:
                    self.try_twilio_auth_create(phone_number)
                    return AuthStatus.EXPIRED

        except TwilioRestException as error:
            if error.status == 429:
                return AuthStatus.TOO_MANY_ATTEMPTS

        return AuthStatus.ERROR
