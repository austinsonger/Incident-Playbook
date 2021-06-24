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
Functions for creating Elasticsearch mappings.

This module provides functions for determining Elasticsearch mappings
based on field types.

========================  ===================================
Function                  Description
========================  ===================================
:func:`~create_mapping`   Get mappings parameter dict.
:func:`~get_data_type`    Get data type for a field type.
:func:`~get_index_types`  Classify fields by indexing method.
========================  ===================================

"""

# third party
from django.conf import settings

# local
from bottler.datafields.models import DataField
from .client import ES_INDEX_SETTINGS, VERSION

_DATE_KEY = settings.DISTILLERIES['DATE_KEY']


def _get_field_mappings():
    """
    Returns a dictionary for creating mappings that work with a newer or
    older version of Elasticsearch.
    """
    if isinstance(VERSION, str) and VERSION < '5.0':
        return {
            'CharField': {
                'type': 'string',
                'index': 'not_analyzed'
            },
            'ChoiceField': {
                'type': 'string',
                'index': 'not_analyzed'
            },
            'ListField': {
                'type': 'string',
                'index': 'not_analyzed'
            },
            'BooleanField': {
                'type': 'boolean',
                'index': 'not_analyzed'
            },
            'DateTimeField': {
                'type': 'date',
                'index': 'not_analyzed',
                'ignore_malformed': True
            },
            'EmailField': {
                'type': 'string',
                'index': 'not_analyzed'
            },
            'FileField': {
                'type': 'string',
                'index': 'not_analyzed'
            },
            'FloatField': {
                'type': 'float',
                'index': 'not_analyzed'
            },
            'IntegerField': {
                'type': 'integer',
                'index': 'not_analyzed'
            },
            'GenericIPAddressField': {
                'type': 'string',
                'index': 'not_analyzed'
            },
            'PointField': {
                'type': 'geo_point',
                'ignore_malformed': True
            },
            'TextField': {
                'type': 'string',
                'index': 'analyzed'
            },
            'URLField': {
                'type': 'string',
                'index': 'not_analyzed'
            }
        }
    else:
        return {
            'CharField': {
                'type': 'keyword',
            },
            'ChoiceField': {
                'type': 'keyword',
            },
            'ListField': {
                'type': 'keyword',
            },
            'BooleanField': {
                'type': 'boolean',
            },
            'DateTimeField': {
                'type': 'date',
                'ignore_malformed': True
            },
            'EmailField': {
                'type': 'keyword',
            },
            'FileField': {
                'type': 'keyword',
            },
            'FloatField': {
                'type': 'float',
            },
            'IntegerField': {
                'type': 'integer',
            },
            'GenericIPAddressField': {
                'type': 'keyword',
            },
            'PointField': {
                'type': 'geo_point',
                'ignore_malformed': True
            },
            'TextField': {
                'type': 'text',
            },
            'URLField': {
                'type': 'keyword',
            }
        }


_MAPPINGS = _get_field_mappings()


def _map_field(mapping, field, properties=None):
    """
    Takes a mapping dictionary, a field name, and a properties dictionary.
    If the field is nested (e.g., 'user.name'), returns a nested mapping
    dictionary.
    """
    fields = field.split('.', 1)

    if properties is None:
        properties = {'properties': {}}

    if 'properties' not in properties:
        properties['properties'] = {}

    # base case: not a nested field
    if len(fields) == 1:
        new_map = {fields[0]: mapping}
        properties['properties'].update(new_map)

    # recursive case: nested field
    else:
        if fields[0] in properties['properties']:
            new_properties = properties['properties'][fields[0]]
            new_map = _map_field(mapping, fields[1], new_properties)
            properties['properties'][fields[0]].update(new_map)
        else:
            new_map = _map_field(mapping, fields[1])
            properties['properties'][fields[0]] = new_map

    return properties


def create_mapping(doc_type, fields):
    """Return a mappings parameter dict for an Elasticsearch index.

    Parameters
    ----------
    doc_type : str
        An Elasticsearch doc_type.

    fields : |list| of |dict|
        List of dictionaries in the form of `{FIELD_NAME_KEY: <field name>,
        FIELD_TYPE_KEY: <field type>}`.

    Returns
    -------
    dict
        Mappings parameter for a doc_type in an Elasticsearch index.

    """
    default = {'type': 'text'}

    # add mapping for the _saved_date field added to every record
    fields.append(DataField(field_name=_DATE_KEY, field_type='DateTimeField'))

    properties = {'properties': {}}
    for field in fields:
        mapping = _MAPPINGS.get(field.field_type, default)
        prop = _map_field(mapping, field.field_name, properties)
        properties.update(prop)

    mappings = {
        'settings': ES_INDEX_SETTINGS,
        'mappings': {
            doc_type: properties
        }
    }

    return mappings


def get_data_type(field_type):
    """Return the data type for a particular field type.

    Identifies the Elasticsearch v5.x data type that corresponds to a
    given Django model field type.

    Parameters
    -------
    field_type : str
        The type of field, e.g. 'CharField'.

    Returns
    -------
    str
        The Elasticsearch data type used to map fields of the given
        field type.

    """
    data_type = _MAPPINGS[field_type]['type']

    # convert Elasticsearch v2.x string types to corresponding v5.x
    # 'keyword' or 'text' types, based on whether the field is analyzed
    if VERSION < '5.0' and data_type == 'string':
        if _MAPPINGS[field_type]['index'] == 'not_analyzed':
            return 'keyword'
        else:
            return 'text'
    else:
        return data_type


def get_index_types(fields):
    """Classify fields as 'text', 'keyword', or 'other'.

    Categorizes |DataFields| according to how they are indexed by
    Elasticsearch. This is useful for determining how to correctly
    query the given fields.

    Parameters
    ----------
    fields : |list| of |DataFields|
        The fields to classify.

    Returns
    -------
    dict
        A dictionary with keys 'text', 'keyword', and 'other' mapped to
        lists of |DataFields| of those types.

    """
    mappings = {
        'text': [],
        'keyword': [],
        'other': []
    }

    for field in fields:
        data_type = get_data_type(field.field_type)
        if data_type in ['text', 'keyword']:
            mappings[data_type].append(field)
        else:
            mappings['other'].append(field)

    return mappings
