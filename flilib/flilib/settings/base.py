import os

from django.contrib.messages import constants as messages
from django.utils.translation import gettext_lazy as _

# Build paths inside the project

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

PROJECT_DIR = os.path.dirname(BASE_DIR)

# Loading secret key

SECRET_KEY_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'secret.key',
)

SECRET_KEY = open(SECRET_KEY_FILE).read().strip()

# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'django_extensions',
    'django_tables2',
    'django_filters',
    'crispy_forms',
    "crispy_bootstrap5",
]

LOCAL_APPS = [
    'core.apps.CoreConfig',
    'library.apps.LibraryConfig',
    'inpx.apps.InpxConfig',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# Middleware to use

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Database

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# URLs
ROOT_URLCONF = 'flilib.urls'

# Template engines

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'flilib.wsgi.application'

# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization

LANGUAGE_CODE = 'ru-ru'

LANGUAGES = [
    ('ru', _('Russian')),
    ('en', _('English')),
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# Bootstrap 5 support

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

DJANGO_TABLES2_TEMPLATE = "django_tables2/bootstrap5.html"

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

# Admin config

ADMIN_SITE_HEADER = _("Flibusta Library administration")

ADMIN_SITE_TITLE = _("Flibusta Library – administration")

ADMIN_INDEX_TITLE = _('Site administration')

# Library config

LIBRARY_DIR = os.path.join(
    PROJECT_DIR,
    'flibusta',
)

INPX_FILE = os.path.join(
    LIBRARY_DIR,
    'flibusta_fb2_local.inpx',
)
