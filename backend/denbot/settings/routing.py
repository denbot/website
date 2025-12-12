"""
This file helps determine what settings we should apply based on our environment.
The .env file is loaded first and is the best place to specify your environment
"""

import logging
import os

from dotenv import load_dotenv

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
