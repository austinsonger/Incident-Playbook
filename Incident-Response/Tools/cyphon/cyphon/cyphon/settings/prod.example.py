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

Production Django settings for Cyphon.

For more information on this Django file, see:
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of Django settings and their values, see:
https://docs.djangoproject.com/en/1.11/ref/settings/

.. _source: ../_modules/cyphon/settings/prod.html

"""

# standard library
import email.utils
import os

# third party
from ec2_metadata import ec2_metadata

# local
from .base import *


#: URL for constructing link with MEDIA_URL, e.g. https://www.example.com
BASE_URL = os.getenv('BASE_URL_PROD', 'http://localhost:8000')

#: Path to directory will logs will be saved.
LOG_DIR = BASE_DIR


###############################################################################
# DJANGO SETTINGS
###############################################################################

#: Whether to enable debug mode.
DEBUG = False

#: A list of all the people who get code error notifications.
ADMINS = [
    # ('Jane Smith', 'jane@example.com'),
]

if 'DJANGO_ADMIN' in os.environ:
    ADMINS.append(email.utils.parseaddr(os.getenv('DJANGO_ADMIN')))

if ON_EC2 or os.getenv('AWS_ACCESS_KEY'):
    INSTALLED_APPS.insert(1, 'django_s3_storage')

#: A logging configuration dictionary.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(name)s '
                      '%(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'WARNING',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'django.log'),
            'when': 'midnight',
            'interval': 1,
            'backupCount': 7,
            'formatter': 'verbose',
        },
        'receiver_file': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'receiver.log'),
            'when': 'midnight',
            'interval': 1,
            'backupCount': 7,
            'formatter': 'verbose',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        },
    },
    'loggers': {
        'django.server': {
            'handlers': ['console', 'file', 'mail_admins'],
            'propagate': True,
            'level': 'WARNING'
        },
        'django.request': {
            'handlers': ['console', 'file', 'mail_admins'],
            'propagate': True,
            'level': 'WARNING'
        },
        'django': {
            'handlers': ['console', 'file', 'mail_admins'],
            'propagate': True,
            'level': 'WARNING',
        },
        'receiver': {
            'handlers': ['console', 'receiver_file', 'mail_admins'],
            'propagate': True,
            'level': 'INFO',
        },
    }
}

#: Default file storage class to be used for any file-related operations
#: that don’t specify a particular storage system.
DEFAULT_FILE_STORAGE = 'django_s3_storage.storage.S3Storage'

#: The file storage engine to use when collecting static files with the
#: collectstatic management command.
STATICFILES_STORAGE = 'django_s3_storage.storage.StaticS3Storage'


###############################################################################
# DJANGO S3 STORAGE
# https://github.com/etianen/django-s3-storage
###############################################################################

# Store media and static content in S3

#: The AWS secret access key to use.
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY')

#: The AWS region to connect to.
if ON_EC2:
    AWS_REGION = ec2_metadata.region
else:
    AWS_REGION = os.getenv('AWS_REGION_NAME', 'us-east-1')

#: The AWS secret access key to use.
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_KEY')

#: Whether to enable authentication for stored files.
AWS_S3_BUCKET_AUTH = False

#: The name of the bucket to store files in.
AWS_S3_BUCKET_NAME = os.getenv('AWS_S3_BUCKET_NAME')

#: The name of the bucket to store static files in.
AWS_S3_BUCKET_NAME_STATIC = AWS_S3_BUCKET_NAME

AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_S3_BUCKET_NAME
AWS_S3_ENDPOINT_URL_STATIC = 'https://s3.amazonaws.com'
AWS_S3_KEY_PREFIX_STATIC = 'static/'

MEDIAFILES_LOCATION = 'media'
STATICFILES_LOCATION = 'static'

# override Django settings
if AWS_S3_BUCKET_NAME:
    MEDIA_ROOT = 'media'
    MEDIA_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)
    STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, STATICFILES_LOCATION)
