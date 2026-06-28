from dataclasses import dataclass
from enum import Enum

from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

from authentication.auth_suppliers.auth_supplier import AuthSupplier
from authentication.enums import AuthStatus
from authentication.exceptions import InvalidConfigError


class TwilioResponse(Enum):
    APPROVED = "approved"
    CANCELED = "canceled"
    DELETED = "deleted"
    FAILED = "failed"
    EXPIRED = "expired"
    MAX_ATTEMPTS_REACHED = "max_attempts_reached"
    PENDING = "pending"


@dataclass(frozen=True)
class TwilioAuthConfig:
    api_key: str
    api_secret: str
    account_sid: str
    service_sid: str


class TwilioAuthSupplier(AuthSupplier):
    def __init__(self, config: TwilioAuthConfig) -> None:
        self._api_key = config.api_key
        self._api_secret = config.api_secret
        self._account_sid = config.account_sid
        self._service_sid = config.service_sid
        self.client = Client(self._api_key, self._api_secret, self._account_sid)

    @classmethod
    def from_settings(cls, options: dict) -> "TwilioAuthSupplier":
        try:
            config = TwilioAuthConfig(**options)
        except TypeError as e:
            raise InvalidConfigError(cls.__name__, e)

        return cls(config)

    def send_code(self, phone_number: str) -> AuthStatus:
        try:
            twilio_response = self.client.verify.v2.services(
                self._service_sid
            ).verifications.create(to=phone_number, channel="sms")
            if twilio_response.status == TwilioResponse.PENDING.value:
                return AuthStatus.CREATED

        except TwilioRestException as error:
            if error.status == 429:
                return AuthStatus.TOO_MANY_ATTEMPTS

        return AuthStatus.ERROR

    def verify_code(self, phone_number: str, verification_code: str) -> AuthStatus:
        try:
            twilio_response = self.client.verify.v2.services(
                self._service_sid
            ).verification_checks.create(to=phone_number, code=verification_code)

            match TwilioResponse(twilio_response.status):
                case TwilioResponse.APPROVED:
                    return AuthStatus.APPROVED
                case TwilioResponse.PENDING:
                    # The Twilio API returns 'pending' when a code is incorrect
                    return AuthStatus.FAILED
                case TwilioResponse.MAX_ATTEMPTS_REACHED:
                    self.send_code(phone_number)
                    return AuthStatus.EXPIRED
                case TwilioResponse.EXPIRED:
                    self.send_code(phone_number)
                    return AuthStatus.EXPIRED
                case _:
                    return AuthStatus.ERROR

        except TwilioRestException as error:
            if error.status == 429:
                return AuthStatus.TOO_MANY_ATTEMPTS

        return AuthStatus.ERROR
