"""
Django settings for DFIRTrack project.
"""

from dfirtrack.config import LOGGING_PATH
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'CHANGEME')

# Application definition

INSTALLED_APPS = [
    'dfirtrack_main',
    'dfirtrack_artifacts',
    'dfirtrack_api',
    'dfirtrack_config',
    'rest_framework',
    'django_q',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.postgres',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework.authtoken',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'dfirtrack_main.async_messages.middleware.async_messages_middleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# use database cache for async messages
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'dfirtrack_async_messages',
    }
}

ROOT_URLCONF = 'dfirtrack.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'dfirtrack.wsgi.application'

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'

LOGIN_REDIRECT_URL = '/system/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'std_formatter': {
            'format': '[%(asctime)s] %(levelname)s %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'handlers': {
        'customlog': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': LOGGING_PATH + '/' + 'dfirtrack.log',
	    'formatter': 'std_formatter',
        },
    },
    'loggers': {
        'dfirtrack_artifacts': {
            'handlers': ['customlog'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'dfirtrack_main': {
            'handlers': ['customlog'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

Q_CLUSTER = {
    'name': 'dfirtrack',
    'orm': 'default',                   # use database backend as message broker
    'label': 'DFIRTrack Q Cluster',     # label for admin page
    'catch_up': False,                  # do not catch up postponed tasks after downtime
    'max_attempts': 1,                  # do not retry failed task
    'timeout': 1800,                    # timeout tasks after half an hour
    'retry': 1801,                      # retry tasks only after timeout time (skip retry is not possible afaik)
    'save_limit': 0,                    # save unlimited successful tasks in the database
    #'sync': True,                       # remove comment for synchronous execution (done for testing via 'dfirtrack.test_settings')
}

REST_FRAMEWORK = {
'DEFAULT_AUTHENTICATION_CLASSES' : [
   'rest_framework.authentication.BasicAuthentication',
   'rest_framework.authentication.SessionAuthentication',
    'dfirtrack_api.authentication.TokenAuthentication',
],
'DEFAULT_PERMISSION_CLASSES': [
       'rest_framework.permissions.IsAuthenticated',
   ],
}

"""
import local settings from local_settings
use settings from this file in case of missing local settings
try statements are splitted to avoid conflicts in case of missing values
"""

# ALLOWED_HOSTS
try:
    from .local_settings import ALLOWED_HOSTS

except ImportError:     # coverage: ignore branch

    # add IP or FQDN if relevant
    ALLOWED_HOSTS = ['localhost']

# DATABASES
try:
    from .local_settings import DATABASES

except ImportError:     # coverage: ignore branch

    # Database - check environment variables for context
    if "CI" in os.environ:
        # use PostgreSQL for GitHub action
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': 'github_actions',
                'USER': 'dfirtrack',
                'PASSWORD': 'dfirtrack',
                'HOST': '127.0.0.1',
                'PORT': '5432',
            }
        }
    else:
        # use SQLite3 otherwise (for local setup without dfirtrack.local_settings)
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join(BASE_DIR, 'dfirtrack.sqlite3'),
            }
        }

# DATA_UPLOAD_MAX_NUMBER_FIELDS
try:
    from .local_settings import DATA_UPLOAD_MAX_NUMBER_FIELDS

except ImportError:     # coverage: ignore branch

    DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000

# DEBUG
try:
    from .local_settings import DEBUG

except ImportError:     # coverage: ignore branch

    # change to True for debugging
    DEBUG = False

# STATIC_ROOT
try:
    from .local_settings import STATIC_ROOT

except ImportError:     # coverage: ignore branch

    STATIC_ROOT = '/var/www/html/static/'
