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

Development Django settings for Cyphon.

For more information on this Django file, see:
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of Django settings and their values, see:
https://docs.djangoproject.com/en/1.11/ref/settings/

.. _source: ../_modules/cyphon/settings/dev.html

"""

# local
from .base import *


#: URL for constructing link with MEDIA_URL.
BASE_URL = os.getenv('BASE_URL_DEV', 'http://localhost:8000')

#: Whether to enable debug mode.
DEBUG = True

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
        'mail_admins': {
            'level': 'WARNING',
            'class': 'django.utils.log.AdminEmailHandler'
        },
    },
    'loggers': {
        'django.server': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'DEBUG'
        },
        'django.request': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'DEBUG'
        },
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'INFO',
        },
        'receiver': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'DEBUG',
        },
    }
}
