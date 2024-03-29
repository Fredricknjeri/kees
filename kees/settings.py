import os
from datetime import timedelta

from .config import * # pylint: disable=unused-wildcard-import,wildcard-import

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INSTALLED_APPS = [
    'core',
    'contrib',
    'webpack_loader',
    'django_nose',
    'crispy_forms',
    'rest_framework.authtoken',
    'rest_framework',
    'reversion',
    'constance',
    'constance.backends.database',
    'django_filters',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'axes',
]

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

NOSE_ARGS = [
    '--with-coverage',
    '--cover-package=core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.middleware.LoginRequiredMiddleware',
    'core.middleware.SetLastVisitMiddleware',
    'axes.middleware.AxesMiddleware',
]

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'

CONSTANCE_ADDITIONAL_FIELDS = {
    'image_field': ['django.forms.ImageField', {}]
}

CONSTANCE_CONFIG = {
    'URL': ('http://localhost:8000', 'Full URL of this instance'),
    'COMPANY_NAME': ('Example', 'Company name'),
    'COMPANY_ADDRESS': ('Example road', 'Company address'),
    'COMPANY_HOUSE_NUMBER': ('1', 'Company house number'),
    'COMPANY_ZIP': ('1234AB', 'Company zip code'),
    'COMPANY_CITY': ('Example city', 'Company city'),
    'LOGO_IMAGE': ('default/logo.svg', 'Logo', 'image_field'),
    'FAVICON_IMAGE': ('default/favicon.png', 'Favicon', 'image_field'),
    'ADDITIONAL_FIELDS': ('', 'Comma separarated list of additional fields that are shown on the case overview page'),
    'ADDITIONAL_FILTERS': ('', 'Comma separarated list of additional filters that are shown on the case overview page'),
    'CREATE_CASE': (True, 'Show option for creating a new case'),
}

CONSTANCE_CONFIG_FIELDSETS = {
    'General Options': (
        'URL',
        'COMPANY_NAME',
        'COMPANY_ADDRESS',
        'COMPANY_HOUSE_NUMBER',
        'COMPANY_ZIP',
        'COMPANY_CITY',
        'LOGO_IMAGE',
        'FAVICON_IMAGE',
        'ADDITIONAL_FIELDS',
        'ADDITIONAL_FILTERS',
        'CREATE_CASE'
    ),
}

CRISPY_TEMPLATE_PACK = 'bootstrap4'

AUTH_USER_MODEL = 'core.User'

AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesBackend',
    'django.contrib.auth.backends.ModelBackend',
]

SESSION_COOKIE_AGE = 3600*24*90 # sessions expire in 90 days

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        }
    }
}

ROOT_URLCONF = 'kees.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'constance.context_processors.config',
            ],
        },
    },
]

WSGI_APPLICATION = 'kees.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    }
]

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher'
]

AXES_COOLOFF_TIME = timedelta(hours=1)
AXES_FAILURE_LIMIT = 25

AXES_PROXY_COUNT = int(os.getenv('AXES_PROXY_COUNT', '1'))
AXES_META_PRECEDENCE_ORDER = [
    'HTTP_X_FORWARDED_FOR',
    'REMOTE_ADDR',
]

AXES_LOCKOUT_CALLABLE = 'core.views.lockout'

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'nl-nl'

TIME_ZONE = 'Europe/Amsterdam'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

WEBPACK_LOADER = {
    'DEFAULT': {
        'STATS_FILE': os.path.join(BASE_DIR, 'frontend', 'webpack-stats.json'),
    }
}

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 25,
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication'
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ],
}

LOGIN_URL = 'login'

LOGIN_REDIRECT_URL = 'dashboard'

LOGIN_EXEMPT_URLS = [
    r'^api/(.+)$',
    r'^media/(.+)$',
    r'^accounts/(.+)$',
    r'^attachments/(\d+)/download/$'
]
