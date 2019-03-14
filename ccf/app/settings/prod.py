import os

from .base import *

SETTINGS_LEVEL = "PROD"

# Database
# Get the ElephantSQL information from the environmental
# variables set by Heroku.
db_user = os.environ.get("DB_NAME")
db_password = os.environ.get("DB_PASSWORD")
db_host = os.environ.get("DB_HOST")

# If any values are falsey, then we cannot create the db with
# prod settings, so use the dev database.
if any([not db_user, not db_password, not db_host]):
    print(
        "Unable to use prod database settings as not all environmental variables are set."
    )
    print("Using default dev database.")
    from .dev import DATABASES
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": db_user,
            "USER": db_user,
            "PASSWORD": db_password,
            "HOST": db_host,
            "PORT": "",
        }
    }

MIDDLEWARE.append("whitenoise.middleware.WhiteNoiseMiddleware")

DEBUG = False
