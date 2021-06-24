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
Creates an Elasticsearch client instance for use in other modules.

=======================  =============================
Constant                 Description
=======================  =============================
:const:`~ELASTICSEARCH`  Elasticsearch client.
:const:`~TIMEOUT`        Request timeout in seconds.
:const:`~VERSION`        Elasticsearch version number.
=======================  =============================

"""

# third party
from django.conf import settings
import elasticsearch


_ES_SETTINGS = settings.ELASTICSEARCH
ES_HOSTS = _ES_SETTINGS.get('HOSTS', ['localhost:9200'])
ES_KWARGS = _ES_SETTINGS.get('KWARGS', {'timeout': 30})
ES_INDEX_SETTINGS = _ES_SETTINGS.get('INDEX', {
    'index.mapping.ignore_malformed': True,
    'number_of_shards': 1,
})

ELASTICSEARCH = elasticsearch.Elasticsearch(ES_HOSTS, **ES_KWARGS)

""":class:`~elasticsearch.Elasticsearch`

Low-level Elasticsearch client. Provides a straightforward mapping from
Python to Elasticsearch REST endpoints.
"""


VERSION = ELASTICSEARCH.info()['version']['number']
"""|str|

The Elasticsearch version number (e.g., '5.2.0').
"""
