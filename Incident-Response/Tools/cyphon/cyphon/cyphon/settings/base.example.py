# -*- coding: utf-8 -*-
# Copyright 2017-2019 ControlScan, Inc.
#
# This file is part of Cyphon Engine.
#
# Cyphon Engine is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# Cyphon Engine is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Cyphon Engine. If not, see <http://www.gnu.org/licenses/>.
"""
[`source`_]

Base Django settings for Cyphon.

For more information on this Django file, see:
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of Django settings and their values, see:
https://docs.djangoproject.com/en/1.11/ref/settings/

.. _source: ../_modules/cyphon/settings/base.html

"""

# standard library
from collections import OrderedDict
from datetime import timedelta
import os
import sys

# local
from .conf import *


###############################################################################
# ISLAND OF MISFIT SETTINGS
###############################################################################

#: URL for REST API.
API_URL = '/api/v1/'

#: URL for REST API.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

#: Directory where Cyphon's dependencies are installed.
REQUIREMENTS = os.path.join(os.path.dirname(BASE_DIR),
                            'virtualenv/lib/python3.4/site-packages')

#: Whether the instance is running in test mode.
TEST = 'test' in sys.argv


###############################################################################
# DJANGO SETTINGS
###############################################################################

#: The host/domain names that this Django site can serve.
ALLOWED_HOSTS = HOST_SETTINGS['ALLOWED_HOSTS']

#: Settings for all databases to be used with Django.
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': POSTGRES['NAME'],
        'USER': POSTGRES['USER'],
        'PASSWORD': POSTGRES['PASSWORD'],
        'HOST': POSTGRES['HOST'],
        'PORT': POSTGRES['PORT'],
    }
}

#: The maximum size in bytes that a request body may be before a
#: SuspiciousOperation (RequestDataTooBig) is raised.
DATA_UPLOAD_MAX_MEMORY_SIZE = 2621440  # i.e., 2.5 MB

#: The maximum number of parameters that may be received via GET or POST
#: before a SuspiciousOperation (TooManyFields) is raised.
DATA_UPLOAD_MAX_NUMBER_FIELDS = 1000

#: Default email address to use for various automated correspondence.
DEFAULT_FROM_EMAIL = EMAIL.get('DEFAULT_FROM', 'webmaster@localhost')

#: The host to use for sending email.
EMAIL_HOST = EMAIL.get('HOST', 'localhost')

#: Password to use for the SMTP server defined in EMAIL_HOST.
EMAIL_HOST_PASSWORD = EMAIL.get('HOST_PASSWORD', '')

#: Username to use for the SMTP server defined in EMAIL_HOST.
EMAIL_HOST_USER = EMAIL.get('HOST_USER', '')

#: Port to use for the SMTP server defined in EMAIL_HOST.
EMAIL_PORT = EMAIL.get('PORT', 25)

#: Subject-line prefix for email messages.
EMAIL_SUBJECT_PREFIX = EMAIL.get('SUBJECT_PREFIX', '[Cyphon] ')

#: Whether to use a TLS (secure) connection when talking to the SMTP server.
EMAIL_USE_TLS = EMAIL.get('USE_TLS', True)

#: A list of all applications that are enabled in this Django installation.
INSTALLED_APPS = [
    'cyphon',  # must come before django.contrib.admin to override templates
    'autocomplete_light',  # must come before django.contrib.admin
    # 'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.gis',
    'django.contrib.messages',
    'django.contrib.postgres',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    # 'debug_toolbar',
    'ckeditor',
    'ckeditor_uploader',
    'constance',
    'constance.backends.database',
    'grappelli.dashboard',  # must come after contenttypes and before grappelli
    'grappelli',  # must come before django.contrib.admin
    'django.contrib.admin',
    'django_extensions',
    'django_filters',
    'django_mailbox',
    'rest_framework',
    'rest_framework_docs',
    'rest_framework_jwt',  # Auth tokens
    'aggregator.filters',
    'aggregator.funnels',
    'aggregator.invoices',
    'aggregator.pipes',
    'aggregator.plumbers',
    'aggregator.pumproom',
    'aggregator.reservoirs',
    'aggregator.samples',
    'aggregator.streams',
    'alerts',
    'ambassador.passports',
    'ambassador.stamps',
    'ambassador.visas',
    'appusers',
    'articles',
    'bottler.containers',
    'bottler.bottles',
    'bottler.labels',
    'bottler.tastes',
    'categories',
    'codebooks',
    'companies',
    'contexts',
    'cyclops',
    'cyphon.settings',
    'distilleries',
    'httmock',
    'inspections',
    'lab.procedures',
    'monitors',
    'notifications',
    'query',
    'query.collectionqueries',
    'query.reservoirqueries',
    'responder.actions',
    'responder.couriers',
    'responder.destinations',
    'responder.dispatches',
    'sifter.datasifter.datachutes',
    'sifter.datasifter.datacondensers',
    'sifter.datasifter.datamungers',
    'sifter.datasifter.datasieves',
    'sifter.logsifter.logchutes',
    'sifter.logsifter.logcondensers',
    'sifter.logsifter.logmungers',
    'sifter.logsifter.logsieves',
    'sifter.mailsifter.mailchutes',
    'sifter.mailsifter.mailcondensers',
    'sifter.mailsifter.mailmungers',
    'sifter.mailsifter.mailsieves',
    'tags',
    'target.followees',
    'target.locations',
    'target.searchterms',
    'target.timeframes',
    'utils.dateutils',
    'utils.geometry',
    'utils.parserutils',
    'utils.validators',
    'warehouses',
    'watchdogs',
]

#: URL that handles the media served from MEDIA_ROOT.
MEDIA_URL = '/media/'

#: Absolute filesystem path to the directory to use for user-uploaded files.
MEDIA_ROOT = os.path.join(HOME_DIR, 'media')

#: A list of middleware to use.
MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'cyphon.version.VersionMiddleware',
)

#: The full Python import path to the root URLconf.
ROOT_URLCONF = 'cyphon.urls'

# Settings for all template engines to be used with Django.
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            '/templates/'
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

#: Path to the WSGI application object used by Django’s built-in server.
WSGI_APPLICATION = 'cyphon.wsgi.application'

# ----------------------------------------------------------------------
# Internationalization and Localization
# https://docs.djangoproject.com/en/1.11/topics/i18n/
# ----------------------------------------------------------------------

#: Language ID code for the default language for this installation.
LANGUAGE_CODE = LOCALIZATION.get('DEFAULT_LANGUAGE', 'en-us')

#: The time zone for this installation.
TIME_ZONE = LOCALIZATION.get('TIME_ZONE', 'UTC')

#: Whether Django’s translation system should be enabled.
USE_I18N = True

#: Whether localized formatting of data will be enabled by default.
USE_L10N = True

#: Whether datetimes will be timezone-aware by default.
USE_TZ = True

# ----------------------------------------------------------------------
# Django Auth
# https://docs.djangoproject.com/en/1.11/topics/auth/
# ----------------------------------------------------------------------

#: Authentication backend classes to use when attempting to authenticate
#: a user.
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',  # this is default
)

#: List of validators that are used to check the strength of user’s passwords.
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 9,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

#: The model to use to represent a User.
AUTH_USER_MODEL = 'appusers.AppUser'

#: Default URL where requests are redirected after login.
LOGIN_REDIRECT_URL = '/app/'

#: The number of days a password reset link is valid for.
PASSWORD_RESET_TIMEOUT_DAYS = 3

# ----------------------------------------------------------------------
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
# ----------------------------------------------------------------------

#: The absolute path to the directory where collectstatic will collect
#: static files for deployment.
STATIC_ROOT = os.path.join(HOME_DIR, 'static')

#: URL to use when referring to static files located in STATIC_ROOT.
STATIC_URL = '/static/'


###############################################################################
# CELERY
# http://docs.celeryproject.org/en/latest/userguide/configuration.html
###############################################################################

#: Default broker URL.
BROKER_URL = 'amqp://{username}:{password}@{host}:5672/{vhost}'.format(
    username=RABBITMQ['USERNAME'],
    password=RABBITMQ['PASSWORD'],
    host=RABBITMQ['HOST'],
    vhost=RABBITMQ['VHOST']
)

#: The periodic task schedule used by beat.
CELERYBEAT_SCHEDULE = {
    'get-new-mail': {
        'task': 'tasks.get_new_mail',
        'schedule': timedelta(seconds=30)
    },
    'run-health-check': {
        'task': 'tasks.run_health_check',
        'schedule': timedelta(seconds=60)
    },
    'run-bkgd-search': {
        'task': 'tasks.run_bkgd_search',
        'schedule': timedelta(seconds=60)
    },
}

#: A white-list of content-types/serializers to allow.
CELERY_ACCEPT_CONTENT = ['json']

#: Result serialization format.
CELERY_RESULT_SERIALIZER = 'json'

#: The default serialization method to use.
CELERY_TASK_SERIALIZER = 'json'

#: Whether the worker pool can be restarted using the pool_restart
#: remote control command.
CELERYD_POOL_RESTARTS = True


###############################################################################
# DJANGO CKEDITOR
# http://django-ckeditor.readthedocs.io/en/latest/
###############################################################################

#: A relative path to the CKEditor media upload directory.
CKEDITOR_UPLOAD_PATH = 'uploads/'

#: Whether to allow upload functionality for non-image files.
CKEDITOR_ALLOW_NONIMAGE_FILES = False


###############################################################################
# DJANGO CONSTANCE
# https://django-constance.readthedocs.io/en/latest/
###############################################################################

#: Backend used to store the configuration values.
CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'

#: Dynamic Django settings.
CONSTANCE_CONFIG = OrderedDict([
    ('PUSH_NOTIFICATIONS_ENABLED', (False, 'Turn on push notifications')),
    ('EMAIL_NOTIFICATIONS_ENABLED', (True, 'Turn on email notifications')),
])

#: Whether to skip hash verification.
CONSTANCE_IGNORE_ADMIN_VERSION_CHECK = True


###############################################################################
# DJANGO GRAPPELLI
# http://django-grappelli.readthedocs.io/en/latest/customization.html
###############################################################################

#: The site title of the admin interface.
GRAPPELLI_ADMIN_TITLE = 'Cyphon'

#: Custom dashboard.
GRAPPELLI_INDEX_DASHBOARD = 'cyphon.dashboard.CyphonIndexDashboard'


###############################################################################
# DJANGO MAILBOX
# http://django-mailbox.readthedocs.io/en/latest/topics/appendix/settings.html
###############################################################################

#: Directory in which to save email attachments.
DJANGO_MAILBOX_ATTACHMENT_UPLOAD_TO = os.path.join(MEDIA_ROOT,
                                                   'mailbox_attachments/%Y/%m/%d/')


###############################################################################
# DJANGO REST FRAMEWORK
# http://www.django-rest-framework.org/api-guide/settings/
###############################################################################

#: Settings for Django REST Framework.
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_METADATA_CLASS': 'rest_framework.metadata.SimpleMetadata',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
        # 'rest_framework.permissions.DjangoModelPermissions',
    ),
    'PAGE_SIZE': 10,
}


###############################################################################
# DJANGO REST FRAMEWORK DOCS
# http://drfdocs.com/settings/
###############################################################################

#: Settings for Django REST Framework Docs.
REST_FRAMEWORK_DOCS = {
    'HIDE_DOCS': os.environ.get('HIDE_DRFDOCS', False)
}


###############################################################################
# DJANGO REST FRAMEWORK JWT AUTH
# https://getblimp.github.io/django-rest-framework-jwt/#additional-settings
###############################################################################

#: Settings for Django REST Framework JWT Auth.
JWT_AUTH = {
    'JWT_ALLOW_REFRESH': True,
    'JWT_EXPIRATION_DELTA': timedelta(weeks=52),
    'JWT_REFRESH_EXPIRATION_DELTA': timedelta(weeks=52),
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'appusers.views.jwt_response_payload_handler',
}
