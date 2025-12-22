from pathlib import Path
from datetime import timedelta
import os


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = "django-insecure-n!-hggli0wd1(2=4!gsrbpt3=px4xxbed$ocvvw2v2+3cq+xz*"
DEBUG = True

INTERNAL_IPS = [
    "127.0.0.1",
]
# list of allowed hosts that can perform requests to django
# matches with host headers in requests
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "vat.berlin-united.com"]

# configures default authentication and permissions
# users need to authenticate with session or token to use any endpoint
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": [
        'rest_framework.permissions.DjangoModelPermissions',
    ],
    # generates API documentation based on the OpenAPI 3.0 standard.
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_RENDERER_CLASSES": (
        "drf_orjson_renderer.renderers.ORJSONRenderer",
        "core.utils.BrowsableAPIRendererWithoutForms",
    ),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}

# Application definition
INSTALLED_APPS = [
    "unfold",
    "unfold.contrib.filters",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_filters",
    "debug_toolbar",
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    "allauth.socialaccount.providers.openid_connect",
    "common",
    "image",
    "annotation",
    "behavior",
    "cognition",
    "motion",
    "frontend",
    "corsheaders",
    "rest_framework",
    "drf_spectacular",
    "rest_framework.authtoken",
    "user",
]
# registers middleware components
# these components process requests before reaching or leaving a view
# the order is very important in this list for more see https://docs.djangoproject.com/en/5.1/ref/middleware/#middleware-ordering
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",

    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "core.middleware.TokenAuthMiddleware",
]
# defines where the url patterns are defined
#'core.urls' means urls.py in the core app
ROOT_URLCONF = "core.urls"

# template stuff. maybe not even requiered since we don't use templates
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

# specifies location of wsgi application
WSGI_APPLICATION = "core.wsgi.application"

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
# loads env variables for database connection
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.getenv("VAT_POSTGRES_DB"),
        "USER": os.getenv("VAT_POSTGRES_USER"),
        "PASSWORD": os.getenv("VAT_POSTGRES_PASS"),
        "HOST": os.getenv("VAT_POSTGRES_HOST"),
        "PORT": os.getenv("VAT_POSTGRES_PORT"),
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

# defines validators for new user passwords
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

SOCIALACCOUNT_ADAPTER = 'user.adapters.KeyCloakRoleGroupAdapter'

SOCIALACCOUNT_PROVIDERS = {
    "openid_connect": {

        "APPS": [
            {
                "provider_id": "keycloak",
                "name": "My Login Server", # https://vat.berlin-united.com/
                "client_id": "VisualAnalytics",
                "secret": os.getenv("VAT_KEYCLOAK_SECRET"),
                "settings": {
                    # When enabled, an additional call to the userinfo
                    # endpoint takes place. The data returned is stored in
                    # `SocialAccount.extra_data`. When disabled, the (decoded) ID
                    # token payload is used instead.
                    "fetch_userinfo": True,
                    "oauth_pkce_enabled": True,
                    #"server_url": "https://my.server.example.com",
                    "server_url": "https://keycloak.berlin-united.com/auth/realms/berlin-united/.well-known/openid-configuration",
                    # Optional token endpoint authentication method.
                    # May be one of "client_secret_basic", "client_secret_post"
                    # If omitted, a method from the the server's
                    # token auth methods list is used
                    "token_auth_method": "client_secret_basic",
                },
            },
        ]
    }
}

HEADLESS_ONLY = True
ACCOUNT_EMAIL_VERIFICATION ="none"

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = False
USE_TZ = True


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' # new
LOGIN_REDIRECT_URL = "/"
SITE_ID = 1 # new

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# For development use (where static files live in the project directories):
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# https://github.com/adamchainz/django-cors-headers

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = ["https://vat.berlin-united.com", "http://localhost:8000", 'http://localhost:3000', "http://127.0.0.1:3000"]

# makes csrf cookie valid on all subdomains
# CSRF_COOKIE_DOMAIN = ".berlin-united.com"
# specifies all domains where django accepts POST requests from with CSRF tokens
CSRF_TRUSTED_ORIGINS = ["https://vat.berlin-united.com", "http://localhost:8000", 'http://localhost:3000', "http://127.0.0.1:3000"]

# requiered if there is a loadbalancer in front of django that forwards requests over http
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# we only want tokenauth in the swagger view
SPECTACULAR_SETTINGS = {
    "AUTHENTICATION_WHITELIST": ["rest_framework.authentication.TokenAuthentication"],
    "SCHEMA_PATH_PREFIX": "/api",
    "SERVERS": [{"url": "https://vat.berlin-united.com"}],
}

# registers our custom user model
AUTH_USER_MODEL = "user.VATUser"

# maximum fields allowed in one post request
DATA_UPLOAD_MAX_NUMBER_FIELDS = 30240

CORS_ALLOW_METHODS = [
    "OPTIONS",
    "POST",
    "PUT",
    "DELETE"
]

# If you need to allow specific headers
CORS_ALLOW_HEADERS = [
    "authorization",
    "content-type",
    "Access-Control-Allow-Credentials",
    "X-CSRFTOKEN"
]


LOGGING = {
    "disable_existing_loggers": False,
    "version": 1,
    "handlers": {
        "console": {
            # logging handler that outputs log messages to terminal
            "class": "logging.StreamHandler",
            "level": "DEBUG",  # message level to be written to console
        },
    },
    "loggers": {
        "": {
            # this sets root level logger to log debug and higher level
            # logs to console. All other loggers inherit settings from
            # root level logger.
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,  # this tells logger to send logging message
            # to its parent (will send if set to True)
        },
        "django.db": {
            # django also has database level logging
            "level": "WARNING"
        },
    },
}
