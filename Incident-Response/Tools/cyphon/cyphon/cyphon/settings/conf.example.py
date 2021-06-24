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


.. _source: ../_modules/cyphon/settings/conf.html

"""

# standard library
import os

# third party
from ec2_metadata import ec2_metadata

# local
from utils.settings import ON_EC2


#: A unique, unpredictable value used to provide cryptographic signing.
SECRET_KEY = 'this-should-be-a-string-of-random-characters'

HOST_SETTINGS = {
    'ALLOWED_HOSTS': [addr.strip() for addr in os.getenv(
        'ALLOWED_HOSTS', 'localhost').split(',')],
}

if ON_EC2:
    HOST_SETTINGS['ALLOWED_HOSTS'].append(ec2_metadata.private_ipv4)

LOCALIZATION = {
    'DEFAULT_LANGUAGE': 'en-us',  # http://www.i18nguy.com/unicode/language-identifiers.html
    'TIME_ZONE': 'UTC',    # https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
}

PAGE_SIZE = 10

PROJ_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
HOME_DIR = os.path.dirname(PROJ_DIR)
KEYS_DIR = os.path.join(HOME_DIR, 'keys')

ALERTS = {
    # Disables searching for alert data in a collection if there is no
    # alert data
    'DISABLE_COLLECTION_SEARCH': False
}

APPUSERS = {
    'CUSTOM_FILTER_BACKENDS': [],
    'ONLY_SHOW_STAFF': False,
}

CODEBOOKS = {
    'CODENAME_PREFIX': '**',  # prefix for displayed CodeNames
    'CODENAME_SUFFIX': '**',  # suffix for displayed CodeNames
}

CYCLOPS = {
    'ENABLED': True,
    'MAPBOX_ACCESS_TOKEN': '',
    'DEVELOPMENT_ENABLED': False,
    'DEVELOPMENT_URL': 'http://localhost:8080/',
    'API_TIMEOUT': 30000,
}

DATASIFTER = {
    'DEFAULT_MUNGER': 'default',
    'DEFAULT_MUNGER_ENABLED': True,
}

DISTILLERIES = {

    # dictionary key for recording the date record was saved
    'DATE_KEY': '_saved_date',

    # dictionary key for saving the primary key of the distillery associated with a
    # distilled document
    'DISTILLERY_KEY': '_distillery',

    # dictionary key for saving fields relating to the location of the raw data on
    # which the distilled data is based
    'RAW_DATA_KEY': '_raw_data',

    # dictionary key for adding a label to a document
    'LABEL_KEY': '_metadata',

    # dictionary key for saving the name of the backend where the raw data is stored
    'BACKEND_KEY': 'backend',

    # dictionary key for saving the name of the database where the raw data is stored
    'WAREHOUSE_KEY': 'database',

    # dictionary key for saving the name of the collection where the raw data is stored
    'COLLECTION_KEY': 'collection',

    # dictionary key for saving the document id for the raw data
    'DOC_ID_KEY': 'doc_id',

    # dictionary key for saving the name of the platform associated with a document
    'PLATFORM_KEY': '_platform',

}

ELASTICSEARCH = {
    'HOSTS': [
        {
            'host': os.getenv('ELASTICSEARCH_HOST', 'elasticsearch'),
            'port': int(os.getenv('ELASTICSEARCH_PORT', '9200')),
            'http_auth': os.getenv('ELASTICSEARCH_HTTP_AUTH'),
            'use_ssl': bool(int(os.getenv('ELASTICSEARCH_USE_SSL', False))),
        },
    ],
    # Note: the keyword arguments provided below are passed to the
    # *Elasticsearch* constructor, and should not contain host-specific
    # keyword arguments for individual connections, which are instead
    # configured in the 'HOSTS' list above.
    'KWARGS': {
        'timeout': 30,
    },
    'INDEX': {
        'index.mapping.ignore_malformed': True,
        'number_of_shards': 1,
    },
}

EMAIL = {
    'DEFAULT_FROM': 'webmaster@localhost',
    'HOST': 'localhost',  # e.g., 'smtp.gmail.com'
    'HOST_USER': '',
    'HOST_PASSWORD': '',
    'PORT': 587,
    'SUBJECT_PREFIX': '[Cyphon] ',
    'USE_TLS': True,
}

FUNCTIONAL_TESTS = {
    'ENABLED': os.getenv('FUNCTIONAL_TESTS_ENABLED', False),
    'DRIVER': os.getenv('FUNCTIONAL_TESTS_DRIVER', 'LOCALHOST'),  # 'DOCKER', 'SAUCELABS'
    'HOST': os.getenv('FUNCTIONAL_TESTS_HOST', 'localhost'),
    'PORT': os.getenv('FUNCTIONAL_TESTS_PORT', '4444'),
    'PLATFORM': os.getenv('FUNCTIONAL_TESTS_PLATFORM', 'ANY'),
    'BROWSER': os.getenv('FUNCTIONAL_TESTS_BROWSER', 'chrome'),
    'VERSION': os.getenv('FUNCTIONAL_TESTS_VERSION', ''),
}

GEOIP = {
    'GEOIP_PATH': os.getenv('GEOIP_PATH', '/usr/share/GeoIP/'),
    'CITY_DB': 'GeoLite2-City.mmdb',
}

JIRA = {
    'SERVER': '',                       # JIRA url
    'PROJECT_KEY': '',                  # project key
    'ISSUE_TYPE': '',                   # issue type
    'CUSTOM_FIELDS': {},                # custom fields
    'PRIORITIES': {
        'CRITICAL': 'Critical',
        'HIGH': 'High',
        'MEDIUM': 'Medium',
        'LOW': 'Low',
        'INFO': 'Low'
    },
    'DEFAULT_PRIORITY': 'Medium',
    'STYLE_PARAMS': {
        'title': 'Cyphon Alert',
        'titleBGColor': '#dcdcdc',
        'bgColor': '#f5f5f5',
    },
    'INCLUDE_FULL_DESCRIPTION': False,
    'INCLUDE_EMPTY_FIELDS': False,
    'INCLUDE_ALERT_COMMENTS': False,
    'INCLUDE_ALERT_LINK': True,
    'COMMENT_VISIBILITY': {
        'type': 'role',
        'value': ''                     # JIRA role
    },
}

LOGSIFTER = {
    'DEFAULT_MUNGER': 'default',
    'DEFAULT_MUNGER_ENABLED': True,
}

MAILSIFTER = {
    'DEFAULT_MUNGER': 'default',
    'DEFAULT_MUNGER_ENABLED': True,
    'MAIL_COLLECTION': 'postgresql.django_cyphon.django_mailbox_message',
    'EMAIL_CONTENT_PREFERENCES': ('text/plain', 'text/html'),
    'ALLOWED_EMAIL_ATTACHMENTS': ('text/plain', 'application/pdf', 'image/jpeg', 'image/png'),
    'ALLOWED_FILE_EXTENSIONS': ('.txt', '.pdf', '.jpeg', '.jpg', '.png'),
    'ATTACHMENTS_FOLDER': 'attachments/%Y/%m/%d/',
}

MONGODB = {
    'HOST': '{0}:{1}'.format(os.getenv('MONGODB_HOST', 'mongo'),  # e.g., 'localhost'
                             os.getenv('MONGODB_PORT', '27017')),
    'TIMEOUT': 20,
}

NOTIFICATIONS = {
    'PUSH_NOTIFICATION_KEY': '',
    'GCM_SENDER_ID': '',
    'IGNORED_ALERT_LEVELS': ['INFO'],
}

POSTGRES = {
    'NAME': os.getenv('POSTGRES_DB', 'postgres'),
    'USER': os.getenv('POSTGRES_USER', 'postgres'),
    'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'postgres'),
    'HOST': os.getenv('POSTGRES_HOST', 'postgres'),  # e.g., 'localhost'
    'PORT': os.getenv('POSTGRES_PORT', '5432'),
}

PRIVATE_FIELDS = [
    DISTILLERIES['DISTILLERY_KEY'],
    DISTILLERIES['RAW_DATA_KEY'],
    DISTILLERIES['DATE_KEY'],
]

RABBITMQ = {
    'HOST': os.getenv('RABBITMQ_DEFAULT_HOST', 'rabbit'),
    'VHOST': os.getenv('RABBITMQ_DEFAULT_VHOST', 'cyphon'),
    'USERNAME': os.getenv('RABBITMQ_DEFAULT_USER', 'guest'),
    'PASSWORD': os.getenv('RABBITMQ_DEFAULT_PASS', 'guest'),
    'EXCHANGE': 'cyphon',
    'DURABLE': True,
}

SAUCELABS = {
    'USERNAME': os.getenv('SAUCE_USERNAME', ''),
    'ACCESS_KEY': os.getenv('SAUCE_ACCESS_KEY', ''),
}

TEASERS = {
    'CHAR_LIMIT': 1000  # Character limit for teaser fields
}

#: Twitter authentication credentials for use in tests
TWITTER = {
    'KEY': '',                          # consumer key
    'SECRET': '',                       # consumer secret
    'ACCESS_TOKEN': '',                 # access token
    'ACCESS_TOKEN_SECRET': '',          # access token secret
}

WAREHOUSES = {
    'DEFAULT_STORAGE_ENGINE': 'elasticsearch'
}
