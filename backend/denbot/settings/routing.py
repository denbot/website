"""
This file helps determine what settings we should apply based on our environment.
The .env file is loaded first and is the best place to specify your environment
"""

import logging
import os
from datetime import timedelta

from dotenv import load_dotenv

from denbot.jwt.keys import JWTSigningKeys

logger = logging.getLogger("denbot")

# Load .env file. All of our settings will be available in os.environ
load_dotenv()

# Determine our environment. If unspecified, we assume the local dev environment to make
#  it easier on developers doing local dev.
env = os.environ.get("ENVIRONMENT", "local")

if env == "local":
    from denbot.settings.local import *  # noqa: F401
elif env == "testing":
    from denbot.settings.testing import *  # noqa: F401
elif env == "prod":
    from denbot.settings.prod import *  # noqa: F401
else:
    raise Exception(f"Unknown environment {env}")

JWT_SIGNING_KEYS: JWTSigningKeys = JWTSigningKeys(
    keys_dir=Path(os.environ.get("JWT_KEYS_DIR", "/storage/keys/jwt")),
    generate_missing_key=env in ["local", "testing"],
)

SIMPLE_JWT = {
    "ALGORITHM": "RS256",
    "VERIFYING_KEY": JWT_SIGNING_KEYS.verifying_key_pem,
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "AUTH_TOKEN_CLASSES": ("denbot.jwt.tokens.DenbotAccessToken",),
}
