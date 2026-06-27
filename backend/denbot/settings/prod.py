import os

from denbot.settings.base import *  # noqa: F401

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")
if SECRET_KEY is None:
    raise Exception("SECRET_KEY must be defined for prod")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["den.bot"]

AUTH_SUPPLIER = {
    "PATH": "authentication.auth_suppliers.twilio_auth_supplier.TwilioAuthSupplier",
    "OPTIONS": {
        "api_key": "TWILIO_API_KEY",
        "api_secret": "TWILIO_API_SECRET",
        "account_sid": "TWILIO_ACCOUNT_SID",
        "service_sid": "TWILIO_SERVICE_SID",
    },
}
