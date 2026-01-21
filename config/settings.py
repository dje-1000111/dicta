import os
from dotenv import load_dotenv, find_dotenv  # type: ignore

load_dotenv(find_dotenv())


ENVIRONMENT = os.getenv("DJANGO_ENV", "dev")

if ENVIRONMENT == "prod":
    from .prod import *  # noqa
else:
    from .dev import *  # noqa
