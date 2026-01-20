import os

# import sentry_sdk
from pathlib import Path
from dotenv import load_dotenv, find_dotenv  # type: ignore
import psycopg2.extensions

# sentry_sdk.init(
#     dsn=os.getenv("SENTRY_DSN"),
#     # integrations=[DjangoIntegration()],
#     # enable_tracing=True,
#     # Set traces_sample_rate to 1.0 to capture 100%
#     # of transactions for performance monitoring.
#     traces_sample_rate=1.0,
#     # Set profiles_sample_rate to 1.0 to profile 100%
#     # of sampled transactions.
#     # We recommend adjusting this value in production.
#     profiles_sample_rate=1.0,
# )


load_dotenv(find_dotenv())

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
RECAPTCHA_PUBLIC_KEY = os.getenv("RECAPTCHA_PUBLIC_KEY")
RECAPTCHA_PRIVATE_KEY = os.getenv("RECAPTCHA_PRIVATE_KEY")
SILENCED_SYSTEM_CHECKS = ["django_recaptcha.recaptcha_test_key_error"]
RECAPTCHA_REQUIRED_SCORE = 0.7
CSRF_FAILURE_VIEW = "apps.dictation.views.csrf_failure"

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "compressor",
    "apps.dictation",
    "apps.dictation_auth",
    "apps.dictation.templatetags.extra_filters",
    "apps.dictation.templatetags.adjusted_elided_page",
    "raven.contrib.django.raven_compat",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "django_recaptcha",
    "django.forms",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "config.middleware.LogErrorsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWD"),
        "PORT": os.getenv("DB_PORT"),
        "DISABLE_SERVER_SIDE_CURSORS": True,
        "TEST": {
            "NAME": "dictation_test_database",
        },
        "OPTIONS": {
            "isolation_level": psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE,
        },
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

AUTHENTICATION_BACKENDS = [
    "apps.dictation_auth.authenticate.EmailModelBackend",
    "django.contrib.auth.backends.ModelBackend",
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = os.getenv("STATIC_ROOT")

# Core Settings
# https://docs.djangoproject.com/en/5.0/ref/settings/
X_FRAME_OPTIONS = "SAMEORIGIN"

LOGIN_URL = "/auth/accounts/login"

# Custom user
AUTH_USER_MODEL = "dictation_auth.User"

# Redirect to profile URL after login (Default redirects to /accounts/profile/)
LOGIN_REDIRECT_URL = "registration/profile.html"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

STATIC_DIR = Path("static")
TXT_DIR = STATIC_DIR / "txt"
IMG_DIR = STATIC_DIR / "img"

PONCTUATION = [
    ".",
    ",",
    ":",
    "!",
    "?",
    ";",
    " - ",
    '"',
    "<",
    ">",
    "/",
    "#",
    "@",
    "$",
    "£",
    "*",
    "¤",
    "|",
    "`",
]
