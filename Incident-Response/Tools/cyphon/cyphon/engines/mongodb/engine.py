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
Defines a MongoDB Engine subclass and related decorators.

======================================  ======================================
Class                                   Description
======================================  ======================================
:class:`~MongoDbEngine`                 Interface for a database collection.
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
:func:`~catch_timeout_error`            Catch ServerSelectionTimeoutErrors.
======================================  ======================================

"""

# standard library
from functools import wraps
import logging

# third party
from bson import ObjectId
from django.conf import settings
import pymongo

# local
from engines.engine import Engine, MAX_RESULTS, PAGE_SIZE
from engines.mongodb import queries as mongodb_queries
from engines.mongodb import sorter as mongodb_sorter
from engines.mongodb import results as mongodb_results
from utils.parserutils import parserutils
from .client import MONGODB_CLIENT

_DISTILLERY_SETTINGS = settings.DISTILLERIES

_LOGGER = logging.getLogger(__name__)


ENGINE_CLASS = 'MongoDbEngine'
"""|str|

The name of the Engine subclass defined in this module.
"""


MULTIPLE_FIELD_NAME_MAPPINGS = True
"""|bool|

Whether the Engine allows fields with the same name to be mapped to
different data types in the same database.
"""


TIME_SERIES_ENABLED = False
"""|bool|

Whether this Engine can store data in a time series, for example, by
creating timestamped collections (e.g. 'logstash-%Y-%m-%d').
"""


def catch_timeout_error(func):
    """Catch and log :exc:`~pymongo.errors.ServerSelectionTimeoutError`.

    Decorator for functions that require a MongoDB connection.
    If a MongoDB request times out, catches and logs the error.

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
        except pymongo.errors.ServerSelectionTimeoutError:
            _LOGGER.error('Cannot connect to MongoDB')
    return _decorator


class MongoDbEngine(Engine):
    """An interface for a MongoDB database collection.

    Provides basic CRUD operations for a particular collection
    within a particular MongoDB database.

    The database and collection are determined by the |Collection|
    used to initialize the Engine instance. The schema is based on
    the |Container| associated with that |Collection|.

    Parameters
    ----------
    collection : |Collection|
        The |Collection| that defines the database and collection of
        the documents to be handled by the Engine. This is also used
        to create a text index for the database collection.

    Attributes
    ----------
    warehouse_collection : Collection
        The |Collection| that defines the database and collection of
        the documents to be handled by the Engine.

    schema : `list` of `DataFields`
        |DataFields| that describe the nature of each field in the
        document type handled by the Engine. Used to create a text index.


    """

    TEXT_INDEXES = ('CharField', 'ListField')

    @catch_timeout_error
    def __init__(self, collection):
        """Initialize a MongoDbEngine instance.

        Creates a MongoDB collection with a text index if one does not
        already exist.
        """
        super(MongoDbEngine, self).__init__(collection)

        self._db_name = self.warehouse_collection.get_warehouse_name()
        self._collection_name = self.warehouse_collection.name
        self._collection = MONGODB_CLIENT[self._db_name][self._collection_name]

        # unique index on _raw_data keys to prevent duplicate docs
        self._create_unique_index()

        if self.schema:
            self._create_text_index(self.schema)

    def __str__(self):
        """Get a string representation of the Engine instance.

        Returns a printable string showing the database and collection.
        """
        return '%s.%s' % (self._db_name, self._collection_name)

    def _create_text_index(self, fields=None):
        """Create a text index for the database collection.

        Takes a list of fields and creates a text index based on the
        Engine's schema, if it has one. Otherwise, creates a text index
        for any field that contains string content.
        """
        collection = self._collection
        index_name = 'TextIndex'

        if fields:
            index = []
            for field in self.schema:
                if field.field_type in self.TEXT_INDEXES:
                    index.append((field.field_name, pymongo.TEXT))
            return collection.create_index(index, background=True,
                                           name=index_name)
        else:
            return collection.create_index([('$**', pymongo.TEXT)],
                                           name=index_name)

    @catch_timeout_error
    def _create_unique_index(self):
        """Create an index based on raw data reference fields.

        Creates a compound index on the fields that contain the location
        of the raw data from which a document was derived. This prevents
        duplicate documents from being saved.
        """
        data_key = _DISTILLERY_SETTINGS['RAW_DATA_KEY']

        fields = [
            'BACKEND_KEY',
            'WAREHOUSE_KEY',
            'COLLECTION_KEY',
            'DOC_ID_KEY'
        ]
        keys = ['%s.%s' % (data_key, _DISTILLERY_SETTINGS[field])
                for field in fields]
        formatted_keys = [(key, pymongo.ASCENDING) for key in keys]
        return self._collection.create_index(formatted_keys, unique=True,
                                             sparse=True)

    @staticmethod
    def _restore_object_id(doc_id):
        """Convert a string to an ObjectId.

        Takes a string representing an ObjectId and returns it as an
        ObjectID instance.
        """
        if isinstance(doc_id, str):
            if 'ObjectId' in doc_id:
                return parserutils.restore_type_from_str(doc_id)
            else:
                return ObjectId(doc_id)
        else:
            return doc_id

    def _restore_object_ids(self, doc_ids):
        """Convert one or more strings to ObjectIds.

        Takes a string representing an ObjectId or a list of strings
        representing ObjectIds. Returns the string(s) as ObjectId(s).
        """
        if isinstance(doc_ids, list):
            return [self._restore_object_id(doc_id) for doc_id in doc_ids]
        else:
            return self._restore_object_id(doc_ids)

    def _get_search_results(self, query, projection=None, sorter=None,
                            page=1, page_size=MAX_RESULTS):
        """Find matching documents.

        Parameters
        ----------
        query : dict
            Search parameters.

        projection : |list| of |str| or None
            The fields to return from matching documents.

        sorter : |Sorter| or |None|
            A |Sorter| defining how results should be ordered.

        page : int
            The page of results to return.

        page_size : int
            The number of documents per page.

        Returns
        -------
        |list| of |dict|
            Documents matching the query.

        """
        offset = self.get_offset(page, page_size)
        query_args = [query]

        if projection:
            query_args.append(projection)

        cursor = self._collection.find(*query_args)

        if sorter:
            m_sorter = mongodb_sorter.MongoDbSorter(sorter.sort_list)
            cursor = cursor.sort(m_sorter.params)

        return cursor.skip(offset).limit(int(page_size))

    def _find_multiple_ids(self, doc_ids):
        """Find documents by their ids.

        Takes a list of hexadecimal document id strings and returns
        the corresponding documents.
        """
        id_filter = mongodb_queries.ids_filter(doc_ids)
        docs = self._get_search_results(id_filter)
        return mongodb_results.get_results(docs)

    def _find_single_id(self, doc_id):
        """Find a document by its id.

        Takes a hexadecimal document id string and returns the
        corresponding document.
        """
        id_filter = mongodb_queries.id_query(doc_id)
        doc = self._collection.find_one(id_filter)
        return mongodb_results.get_results(doc)

    @catch_timeout_error
    def find_by_id(self, doc_ids):
        """Find one or more documents by id.

        Parameters
        ----------
        doc_ids : |str| or |list| of |str|
            A hexadecimanl document id or a list of ids.

        Returns
        -------
        |dict|, |list| of |dict|, or |None|
            Documents corresponding to the given id(s). Returns a list
            of documents if doc_ids is a list; otherwise returns a
            single document. If no matches are found, returns `None`.

        """
        obj_ids = self._restore_object_ids(doc_ids)

        if isinstance(obj_ids, list):
            data = self._find_multiple_ids(obj_ids)
        else:
            data = self._find_single_id(obj_ids)

        return data or None

    @catch_timeout_error
    def find(self, query, sorter=None, page=1, page_size=PAGE_SIZE):
        """Find documents matching a query.

        Parameters
        ----------
        query : |EngineQuery|
            An |EngineQuery| defining critieria for matching documents.

        sorter : |Sorter| or |None|
            A |Sorter| defining how results should be ordered.

        page : int
            The page of results to return.

        page_size : int
            The number of documents per page of results.

        Returns
        -------
        |list| of |dict|
            A dictionary with keys 'count' and 'results'. The 'count'
            value is the total number of documents matching the search
            criteria. The 'results' value is a list of documents from
            the search result, with the doc ids added to each document.

        """
        query = mongodb_queries.MongoDbQuery(query.subqueries, query.joiner)
        projection = self.field_names
        mongodb_params = query.params
        docs = self._get_search_results(mongodb_params, projection, sorter,
                                        page, page_size)
        return mongodb_results.get_results_and_count(docs)

    @catch_timeout_error
    def filter_ids(self, doc_ids, fields, value):
        """Find the ids of documents that match a value.

        Parameters
        ----------
        doc_ids : |list| of |str|
            Hexadecimal ids of documents to filter.

        fields : |list| of |DataField|
            |DataFields| that should be examined for a matching value.

        value : str
            A value used to find matching documents.

        Returns
        -------
        |list| of |str|
            The subset of hexadecimal ids for documents containing the
            given `value` in one or more of the specified `fields`.

        """
        obj_ids = self._restore_object_ids(doc_ids)
        query = mongodb_queries.ids_and_value_filter(obj_ids, fields, value)
        projection = {}  # only return ObjectIds
        results = self._get_search_results(query, projection)
        return mongodb_results.get_doc_ids(results)

    def insert(self, doc):
        """Insert the document into the collection.

        Parameters
        ----------
        doc : dict
            A document to insert into the MongoDB collection.

        Returns
        -------
        str
            The hexadecimal id of the inserted document.

        Notes
        ------
        If a document with the same key already exists, catches the
        :class:`~pymongo.errors.DuplicateKeyError` and returns the id
        of the original document.

        """
        try:
            inserted_result = self._collection.insert_one(doc)
            obj_id = inserted_result.inserted_id

        except pymongo.errors.DuplicateKeyError as error:
            errmsg = error.details['errmsg']
            key_val = parserutils.get_dup_key_val(errmsg)
            dup = self._collection.find_one(key_val)
            obj_id = dup['_id']

        return str(obj_id)

    def remove_by_id(self, doc_ids):
        """Remove the documents with the given ids.

        Parameters
        ----------
        doc_ids : |str| or |list| of |str|
            A hexadecimal id or list of ids of documents to remove
            from the collection.

        Returns
        -------
        None

        """
        doc_ids = self._restore_object_ids(doc_ids)
        if isinstance(doc_ids, list):
            id_filter = mongodb_queries.ids_filter(doc_ids)
            return self._collection.delete_many(id_filter)
        else:
            id_filter = mongodb_queries.id_query(doc_ids)
            return self._collection.delete_one(id_filter)
