import os

from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

api_key = os.environ["TWILIO_API_KEY"]
api_secret = os.environ["TWILIO_API_SECRET"]
account_sid = os.environ["TWILIO_ACCOUNT_SID"]
service_sid = os.environ["TWILIO_SERVICE_SID"]
client = Client(api_key, api_secret, account_sid)


def try_twilio_auth_create(phone_number: str) -> str:
    status = "error"
    try:
        twilio_response = client.verify.v2.services(service_sid).verifications.create(
            to=phone_number, channel="sms"
        )
        match twilio_response.status:
            case "pending":
                status = "created"
            case _:
                status = "error"
    except TwilioRestException as error:
        if error.status == 429:
            status = "too_many_attempts"
        else:
            status = "error"
    return status


def try_twilio_auth_verify(phone_number: str, verification_code: str) -> str:
    status = "error"
    try:
        twilio_response = client.verify.v2.services(
            service_sid
        ).verification_checks.create(to=phone_number, code=verification_code)

        match twilio_response.status:
            case "approved":
                status = "approved"
            case "pending":
                status = "failed"
            case "max_attempts_reached":
                try_twilio_auth_create(phone_number)
                status = "expired"
            case "expired":
                try_twilio_auth_create(phone_number)
                status = "expired"
            case _:
                status = "error"

    except TwilioRestException as error:
        if error.status == 429:
            status = "too_many_attempts"
        else:
            status = "error"
    return status
