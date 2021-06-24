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
Defines classes and helper functions for constructing MongoDB queries.

====================================  =========================================
Class                                 Description
====================================  =========================================
:class:`~MongoDbQuery`                Create a query for MongoDB.
:class:`~MongoDbQueryFieldset`        Format a |QueryFieldset| for MongoDB.
====================================  =========================================

====================================  =========================================
Function                              Description
====================================  =========================================
:func:`~id_query`                     Create a query to find a doc by id.
:func:`~ids_and_value_filter`         Create a query for docs matching a value.
:func:`~ids_filter`                   Create a filter for docs using ids.
:func:`~regex_query`                  Create a regex query.
====================================  =========================================

"""

# standard library
import json
import re

# local
from engines.queries import EngineQueryFieldset, EngineQuery
from utils.parserutils.parserutils import restore_type

# map logical operators to those used by MongoDB
_MONGODB_QUERY_JOINERS = {
    'OR': '$or',
    'AND': '$and'
}


def regex_query(field_name, value):
    """Create a regex query.

    Constructs a MongoDB regex query that will match documents in which
    the specified value is found somewhere within the content of the
    given field.

    Parameters
    ----------
    field_name : str
        The name of the field to be queried.

    value : str
        A value that should appear somewhere in the field's content.

    Returns
    -------
    dict
        A MongoDB regexp query.

    """
    return {field_name: {'$regex': value, '$options': 'i'}}


def ids_filter(doc_ids):
    """Create a filter for documents with the given ids.

    Parameters
    ----------
    doc_id : |list| of |ObjectIds|
        The document ids to match.

    Returns
    -------
    dict
        A query for documents matching the given `doc_ids`.

    """
    return {'_id': {'$in': doc_ids}}


def id_query(doc_id):
    """Create a query for a document with the given id.

    Parameters
    ----------
    doc_id : |ObjectId|
        The document id to match.

    Returns
    -------
    dict
        A query for a document with the given `doc_id`.

    """
    return {'_id': doc_id}


def ids_and_value_filter(obj_ids, fields, value):
    """Create a query to find documents that contain the given value.

    Constructs a query that will find documents associated with the set
    of `doc_ids` that also contain the given `value` somewhere within
    the content of one of the given `fields`.

    Parameters
    ----------
    doc_ids : |list| of |str|
        The document ids to match.

    fields : |list| of |DataFields|
        |DataFields| indicating the fields in documents that should be
        examined for a matching value.

    value : |str|
        A value used to find matching documents.

    Returns
    -------
    list
        Document ids for which at least one of the specified `fields`
        contains the given `value`.

    """
    query = ids_filter(obj_ids)
    regex_q = [regex_query(field.field_name, value) for field in fields]
    query.update({_MONGODB_QUERY_JOINERS['OR']: regex_q})
    return query


class MongoDbQueryFieldset(EngineQueryFieldset):
    """Format a |QueryFieldset| for MongoDB.

    Parameters
    ----------
    fieldset : |QueryFieldset|
        A |QueryFieldset| providing the basis for a query expression.

    Attributes
    ----------
    field_name : str
        The name of the field being queried.

    field_type : str
        The type of field being queried (e.g., 'CharField'). Corresponds
        to a value in |FIELD_TYPE_CHOICES|.

    raw_value : str
        The `value` from the |QueryFieldset| used to initialize the
        object instance.

    raw_operator : str
        The `operator` from the |QueryFieldset| used to initialize the
        object instance. Corresponds to a value in |OPERATOR_CHOICES|.

    operator : str
        The engine-specific operator that should be used for building
        the query expression.

    negate : bool
        Indicates whether the `operator` should be negated by applying
        'NOT' logic to the query expression.

    value : |str|, |int|, |float|, |dict|, or |list|
        The value that should be used in the query expression, to be
        compared against the value of the field being queried.

    """

    QUERY_OPERATORS = {
        'eq': '$eq',                    # equals
        'in': '$in',                    # list contains value
        'gt': '$gt',                    # greater than
        'gte': '$gte',                  # greater than or equal to
        'lt': '$lt',                    # less than
        'lte': '$lte',                  # less than or equal to
        'regex': '$regex',              # text contains regex
        'not:eq': '$ne',                # does not equal
        'not:in': '$nin',               # list does not contain value
        'not:regex': '$not:$regex',     # text does not contain regex
        'not:missing': '$ne:None',      # is not null
        'within': '$geoWithin'          # within polygon(s)
    }
    """|dict|

    Maps the values in |OPERATOR_CHOICES| to the corresponding
    query operators in MongoDB.
    """

    QUERY_JOINERS = _MONGODB_QUERY_JOINERS
    """|dict|

    Maps the values in |LOGIC_CHOICES| to the corresponding query
    operators in MongoDB.
    """

    NEGATE_OPERATOR = '$not:'
    """|dict|

    The Engine's equivalent of a 'NOT' operator. Used for negating a
    |QueryFieldset|.
    """

    def format_value(self):
        """Format a value for a query expression.

        Transforms the `raw_value` attribute into a value that can be
        used in a MongoDB query expression.

        Returns
        -------
        |str|, |int|, |float|, |dict|, or |list|
            A value that can be used in the query expression.

        """
        value = restore_type(self.field_type, self.raw_value)
        if self.operator == '$regex':
            return re.compile(value, re.IGNORECASE)
        elif self.operator == '$geoWithin':
            return json.loads(value)
        elif self.operator in ['$in', '$nin']:
            return [value]  # MongoDB requires array here
        else:
            return value

    def _polygon_filter(self, polygon_feature):
        """Create a polygon filter.

        Takes a GeoJSON polygon or multipolygon feature and returns
        a $geoWithin filter for that field.
        """
        geometry = polygon_feature['geometry']

        if geometry['type'] not in ['Polygon', 'MuliPolygon']:  # pragma: no cover
            raise ValueError('Feature is a %s not a Polygon or MuiltPolygon'
                             % geometry['type'])

        return {
            self.field_name: {
                '$geoWithin': {
                    '$geometry': polygon_feature['geometry']
                }
            }
        }

    def _regex_query(self):
        """Create a regex query.

        Returns a selector for matching a field using a regular
        expression.
        """
        if self.negate:
            return {self.field_name: {'$not': self.value}}
        else:
            return regex_query(self.field_name, self.value)

    def _not_null_query(self):
        """Create a query for a non-null value.

        Returns a query that matches documents in which a field
        is not null.
        """
        return {self.field_name: {'$ne': None}}

    def _default_query(self):
        """Create a generic query.

        Returns a generic field query.
        """
        return {self.field_name: {self.operator: self.value}}

    @property
    def selector(self):
        """Create a query expression.

        Creates a dictionary suitable for use as a selector in a
        MongoDB query.

        Returns
        -------
        dict
            A query expression based on the |QueryFieldset| used to
            initialize the object instance.

        """
        query_functions = {
            '$ne:None': self._not_null_query,
            '$geoWithin': self._geo_query,
            '$regex': self._regex_query
        }
        query_function = query_functions.get(self.operator, self._default_query)
        return query_function()


class MongoDbQuery(EngineQuery):
    """Create a query for MongoDB.

    Defines search parameters for querying the database and collection
    serviced by a |MongoDBEngine| instance. Uses those parameters to
    format a MongoDB query.

    Attributes
    ----------
    subqueries : list of QueryFieldsets and/or EngineQueries
        Any combination of |QueryFieldsets| and child |EngineQueries|
        to be used in constructing a query. Child |EngineQueries| are
        used to construct more complex (nested) query expressions.

    joiner : str
        A logical operator for combining query terms. Corresponds to a
        value in |LOGIC_CHOICES|.

    """

    QUERY_JOINERS = _MONGODB_QUERY_JOINERS
    """|dict|

    Maps the values in |LOGIC_CHOICES| to the corresponding logical
    operators in MongoDB.
    """

    fieldset_model = MongoDbQueryFieldset
    """|type|

    The |EngineQueryFieldset| subclass used to model fieldsets for
    MongoDB.
    """
