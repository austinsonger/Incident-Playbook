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
Defines an Elasticsearch Engine subclass and related decorators.

======================================  ======================================
Class                                   Description
======================================  ======================================
:class:`~ElasticsearchEngine`           Interface for an index and doc_type.
======================================  ======================================

======================================  ======================================
Constant                                Description
======================================  ======================================
:const:`~ENGINE_CLASS`                  Name of module's Engine subclass.
:const:`~MULTIPLE_FIELD_NAME_MAPPINGS`  Whether a field can have >1 data type.
:const:`~TIME_SERIES_ENABLED`           Whether time-series are supported.
======================================  ======================================

======================================  ======================================
Decorator                               Description
======================================  ======================================
:func:`~catch_connection_error`         Catch and log ConnectionErrors.
:func:`~wait_for_status`                Wait for a certain cluster state.
======================================  ======================================

"""

# standard library
import datetime
from functools import wraps
import logging

# third party
from django.utils import timezone
import elasticsearch

# local
from engines.elasticsearch import queries as es_queries
from engines.elasticsearch import results as es_results
from engines.elasticsearch import sorter as es_sorter
from engines.engine import Engine, MAX_RESULTS, PAGE_SIZE
from .client import ELASTICSEARCH, ES_KWARGS
from .mapper import create_mapping

_LOGGER = logging.getLogger(__name__)

TIMEOUT = ES_KWARGS.get('timeout', 30)

ENGINE_CLASS = 'ElasticsearchEngine'
"""|str|

The name of the Engine subclass defined in this module.
"""


MULTIPLE_FIELD_NAME_MAPPINGS = False
"""|bool|

Whether the Engine allows fields with the same name to be mapped to
different data types in the same index.
"""


TIME_SERIES_ENABLED = True
"""|bool|

Whether this Engine can store data in a time series, for example, by
creating timestamped indexes (e.g. 'logstash-%Y-%m-%d'). This is used
for easily archiving or deleting old data.
"""


def catch_connection_error(func):
    """Catch and log :exc:`~elasticsearch.exceptions.ConnectionError`.

    Decorator for functions that require an Elasticsearch connection.
    If a connection cannot be established, catches and logs the error.

    Parameters
    ----------
    func : function
        The function to modify.

    Returns
    -------
    function
        The modified function.

    """
    @wraps(func)  # preserve name and docstring of wrapped function
    def _decorator(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except elasticsearch.exceptions.ConnectionError:
            _LOGGER.error('Cannot connect to Elasticsearch')
    return _decorator


def wait_for_status(status, timeout=TIMEOUT):
    """
    Wait for a particular Elasticsearch cluster status.

    Decorator for functions that require a particular cluster state.
    Waits for the cluster to attain the given status before executing
    the function.

    Parameters
    ----------
    status : str
        The desired cluster state. Options are: 'green', 'yellow', 'red'.

    timeout : |int| or |float|
        The number of seconds to wait for the desired state.

    Returns
    -------
    function
        The modified function.

    """
    def _decorator(func):
        @wraps(func)  # preserve name and docstring of wrapped function
        def _call(*args, **kwargs):
            ELASTICSEARCH.cluster.health(wait_for_status=status,
                                         request_timeout=timeout)
            return func(*args, **kwargs)
        return _call
    return _decorator


class ElasticsearchEngine(Engine):
    """An interface for an Elasticsearch index and doc_type.

    Provides basic CRUD operations for a particular document type
    within a particular Elasticsearch index or time series
    (e.g., 'logstash-%Y-%m-%d').

    The index and doc_type are determined by the |Collection| used
    to initialize the Engine instance. The mapping is based on the
    |Container| associated with that |Collection|.

    Parameters
    ----------
    collection : |Collection|
        The |Collection| that defines the index and doc_type of the
        documents to be handled by the Engine. This is also used to
        determine the mapping.

    Attributes
    ----------
    warehouse_collection : Collection
        The |Collection| that defines the index and doc_type of the
        documents to be handled by the Engine.

    schema : `list` of `DataFields`
        |DataFields| that describe the nature of each field in the
        document type handled by the Engine. Used to create a mapping.

    """

    @catch_connection_error
    @wait_for_status('yellow')
    def __init__(self, collection):
        """Initialize an ElasticsearchEngine instance.

        Creates an Elasticsearch index with the Engine's index name
        and a mapping defined by the Engine's schema, if one does not
        already exist.
        """
        super(ElasticsearchEngine, self).__init__(collection)
        self._index_name = self.warehouse_collection.get_warehouse_name()
        self._doc_type = self.warehouse_collection.name
        self._in_time_series = self.warehouse_collection.in_time_series()

        if not self._in_time_series and not self._index_exists():
            self._create_index()

    def __str__(self):
        """Get a string representation of the Engine instance.

        Returns a printable string showing the index and doc_type.
        """
        return '%s.%s' % (self._index_name, self._doc_type)

    @staticmethod
    def _current_date():
        """Get the current date.

        Returns the current timezone-aware date as a string in ISO format.
        """
        current_dt = timezone.now()
        current_date = datetime.date(current_dt.year, current_dt.month,
                                     current_dt.day)
        return current_date.isoformat()

    @property
    def _index_for_insert(self):
        """Get the name of the index for inserting docs.

        Returns the name of the index into which new documents should be
        inserted. If the index belongs to a time series, the index name
        will include the current date in ISO format.
        """
        if self._in_time_series:
            return self._index_name + '-' + self._current_date()
        else:
            return self._index_name

    @property
    def _params_for_insert(self):
        """Create basic parameters for inserting docs.

        Returns a dictionary with a base set of parameters for inserting
        new documents. These parameters specify the index and doc_type
        under which new documents should be inserted.
        """
        return {'index': self._index_for_insert, 'doc_type': self._doc_type}

    @property
    def _index_for_search(self):
        """Get the index name or pattern for searching docs.

        Returns the name of the index(es) that should be used in document
        searches. If the Engine represents a time series of indexes,
        the name will contain wildcards so that all indexes belonging
        to the time series will be included in a search.
        """
        if self._in_time_series:
            return self._index_name + ',' + self._index_name + '-*-*-*'
        else:
            return self._index_name

    @property
    def _index_for_template(self):
        """Get the index name or pattern for creating a template."""
        if self._in_time_series:
            return self._index_name + '-*-*-*'
        else:
            return self._index_name

    @property
    def _params_for_search(self):
        """Create basic parameters for searching docs.

        Returns a dictionary with a base set of parameters for searching
        documents. These parameters specify the index and doc_type that
        should be searched.
        """
        return {'index': self._index_for_search, 'doc_type': self._doc_type}

    def _index_exists(self):
        """Find out if the index already exists.

        Returns a Boolean indicating whether the index containing the
        Engine's doc_type already exists.
        """
        return ELASTICSEARCH.indices.exists(self._index_for_insert)

    def _create_mapping(self):
        """Create a mapping for the index.

        Returns a dict of properties for mapping the data fields in
        Elasticsearch.
        """
        return create_mapping(self._doc_type, self.schema)

    def _create_index(self):
        """Create an index for inserting docs.

        Creates an Elasticsearch index with the Engine's index name and
        a mapping defined by the Engine's schema.
        """
        index = self._index_for_insert
        mappings = self._create_mapping()
        params = {'index': index, 'ignore': 400, 'body': mappings}
        ELASTICSEARCH.indices.create(**params)

    def create_template(self):
        """Create a template for the index.

        Returns a dict of properties for an Elasticsearch index template.
        """
        name = str(self)
        body = self._create_mapping()
        body.update({'template': self._index_for_template})
        if ELASTICSEARCH.indices.exists_template(name):
            ELASTICSEARCH.indices.delete_template(name)
        ELASTICSEARCH.indices.put_template(name=name, body=body)

    def _filter_by_id(self, doc_ids):
        """Get docs matching one or more ids from multiple indexes.

        Takes a document id or a list of document ids, and returns
        documents matching the given id(s) from indexes associated with
        the Engine instance. Used to locate documents across multiple
        indexes, as in the case of a time series (timestamped indexes).
        """
        is_list = isinstance(doc_ids, list)
        if not is_list:
            doc_ids = [doc_ids]

        params = self._params_for_search
        query = es_queries.ids_query(doc_ids)
        params.update({
            'body': query, '_source': True,
            'ignore_unavailable': True
        })
        results = ELASTICSEARCH.search(**params)
        formatted_results = es_results.get_source(results)
        if is_list:
            return formatted_results
        elif len(formatted_results) > 0:
            return formatted_results[0]

    def _find_multiple_ids(self, doc_ids):
        """Get docs matching a list of ids from an index.

        Takes a list of document ids and returns a list of matching
        documents from the index associated with the Engine.
        """
        params = self._params_for_search
        params.update({'body': {'ids': doc_ids}, 'refresh': True})
        results = ELASTICSEARCH.mget(**params)
        return es_results.get_found_docs(results)

    def _find_single_id(self, doc_id):
        """Get a doc matching an id from an index.

        Takes a document id and returns the matching document from the
        index associated with the Engine.
        """
        params = self._params_for_search
        query = es_queries.id_query(doc_id)
        params.update(query)
        result = ELASTICSEARCH.get(**params)
        if result['found']:
            return es_results.get_source_with_id(result)

    def _get_search_results(self, query, source, size=MAX_RESULTS, offset=0):
        """Return the raw search result from the Elasticsearch API.

        Parameters
        ----------
        query : dict
            Query parameters.

        source : |bool| or |list| of |str|
            |True| or |False| to return the _source field or not, or a
            list of specific fields to return.

        size : int
            The maximum number of results to return.

        offset : int
            The number of results to skip when returning the result set.

        Returns
        -------
        dict
             The raw result from the Elasticsearch API.

        """
        params = self._params_for_search

        params.update({
            'body': query,
            '_source': source,
            'size': size,
            'from_': offset,
            'ignore_unavailable': True,
        })

        return ELASTICSEARCH.search(**params)

    @catch_connection_error
    @wait_for_status('yellow')
    def find_by_id(self, doc_ids):
        """Find one or more documents by id.

        Parameters
        ----------
        doc_ids : |str| or |list| of |str|
            A document id or a list of document ids.

        Returns
        -------
        |dict|, |list| of |dict|, or |None|
            Documents corresponding to the given id(s). Returns a list
            of documents if doc_ids is a list; otherwise returns a
            single document. If no matches are found, returns `None`.

        """
        if self._in_time_series:
            return self._filter_by_id(doc_ids)
        elif isinstance(doc_ids, list):
            return self._find_multiple_ids(doc_ids) or None
        else:
            return self._find_single_id(doc_ids)

    @catch_connection_error
    @wait_for_status('yellow')
    def find(self, query, sorter=None, page=1, page_size=PAGE_SIZE):
        """Find documents matching a query.

        Parameters
        ----------
        query : |EngineQuery|
            An |EngineQuery| defining critieria for matching documents
            in the index or time series.

        sorter : |Sorter| or |None|
            A |Sorter| defining how results should be ordered.

        page : int
            The page of results to return.

        page_size : int
            The number of documents per page of results.

        Returns
        -------
        |dict|
            A dictionary with keys 'count' and 'results'. The 'count'
            value is the total number of documents matching the search
            criteria. The 'results' value is a list of documents from
            the search result, with the doc ids added to each document.

        """
        offset = self.get_offset(page, page_size)
        es_query = es_queries.ElasticsearchQuery(query.subqueries,
                                                 query.joiner)
        params = es_query.params

        if sorter:
            elastic_sorter = es_sorter.ElasticsearchSorter(sorter.sort_list)
            params.update(elastic_sorter.params)

        results = self._get_search_results(
            params,
            source=self.field_names,
            size=page_size,
            offset=offset
        )
        return es_results.get_results_and_count(results)

    @catch_connection_error
    @wait_for_status('yellow')
    def filter_ids(self, doc_ids, fields, value):
        """Find the ids of documents that match a value.

        Parameters
        ----------
        doc_ids : |list| of |str|
            The ids of documents to filter.

        fields : |list| of |DataFields|
            |DataFields| that should be examined for a matching value.

        value : str
            A value used to find matching documents.

        Returns
        -------
        |list| of |str|
            The subset of ids for documents containing the given `value`
            in one or more of the specified `fields`.

        """
        query = es_queries.ids_and_value_filter(doc_ids, fields, value)
        results = self._get_search_results(query, source=False)
        return es_results.get_doc_ids(results)

    def insert(self, doc):
        """Insert the document into the index.

        Parameters
        ----------
        doc : dict
            A document to insert into the Elasticsearch index.

        Returns
        -------
        str
            The id of the inserted document.

        """
        params = self._params_for_insert
        params.update({'body': doc, 'refresh': True})
        if not self._index_exists():
            self._create_index()
        doc = ELASTICSEARCH.index(**params)
        return doc['_id']

    def _remove_by_id_wildcard(self, doc_ids):
        """Remove one or more docs from multiple indexes.

        Takes a document id or a list of document ids and removes the
        document(s) from the Elasticsearch index(es) associated with the
        Engine. Used for removing documents from time series indexes.
        """
        params = self._params_for_search
        query = es_queries.ids_query(doc_ids)
        params.update({
            'body': query,
            '_source': False,
            'ignore_unavailable': True
        })
        results = ELASTICSEARCH.search(**params)

        for hit in es_results.get_hits(results):
            params = es_results.get_doc_info(hit)
            params.update({'refresh': True})
            ELASTICSEARCH.delete(**params)

    def _remove_by_id_simple(self, doc_ids):
        """Remove one or more docs from an index.

        Takes a document id or a list of document ids and removes the
        document(s) from the Elasticsearch index associated with the
        Engine.
        """
        for doc_id in doc_ids:
            params = self._params_for_search
            query = es_queries.id_query(doc_id)
            params.update(query)
            ELASTICSEARCH.delete(**params)

    @catch_connection_error
    @wait_for_status('yellow')
    def remove_by_id(self, doc_ids):
        """Remove the documents with the given ids.

        Parameters
        ----------
        doc_ids : |str| or |list| of |str|
            An id or list of ids of documents to remove from the index.

        Returns
        -------
        None

        """
        if not isinstance(doc_ids, list):
            doc_ids = [doc_ids]

        if self._in_time_series:
            return self._remove_by_id_wildcard(doc_ids)
        else:
            return self._remove_by_id_simple(doc_ids)
