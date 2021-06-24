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
Provides a base |Engine| class for interacting with data stores.

An |Engine| performs CRUD operations on a set of documents in a data
store, represented by a |Collection|. Essentially, an |Engine| shuttles
documents to and from that |Collection|.

=====================  =================================================
Class                  Description
=====================  =================================================
:class:`~Engine`       Interface for a data store.
=====================  =================================================

=====================  =================================================
Constant               Description
=====================  =================================================
:const:`~MAX_RESULTS`  Maximum number of results to return for a search.
=====================  =================================================

"""

# third party
from django.conf import settings

# local
from cyphon.baseclass import BaseClass

PAGE_SIZE = settings.PAGE_SIZE

MAX_RESULTS = 1000
"""|int|

Maximum number of results to return from a query.
"""


class Engine(BaseClass):
    """An interface for a data store.

    Base class used to define subclasses for interacting with specific
    data stores (such as MongoDB or Elasticsearch).

    An Engine performs CRUD operations on a set of documents in a
    data store that are represented by a |Collection|. The |Collection|
    can correspond to any one of the following:

        - a table in a relational database
        - a collection in a NoSQL database
        - a document type in a search engine index

    Essentially, an Engine shuttles documents to and from a storage
    location. It can insert or remove documents from that location and
    fetch query results.

    Parameters
    ----------
    collection : |Collection|
        The |Collection| that determines both the schema and the storage
        location of the documents to be handled by the Engine instance.

    Attributes
    ----------
    warehouse_collection : Collection
        The |Collection| that defines the storage location of the
        documents to be handled by the Engine instance.

    schema : `list` of `DataFields`
        |DataFields| that describe the nature of each field in the
        document type handled by the Engine.

    """

    def __init__(self, collection):
        """Initialize an Engine instance."""
        self.warehouse_collection = collection
        self.schema = collection.get_schema()

    @property
    def field_names(self):
        """List the fields in the Engine's schema.

        Returns
        -------
        |list| of |str|
            Field names for fields in the Engine's schema. Nested fields
            are denoted using dot notation (e.g., "user.screen_name").

        """
        return [field.field_name for field in self.schema]

    @staticmethod
    def get_offset(page, page_size):
        """Get the number of documents to skip when returning results.

        Parameters
        ----------
        page : int
            The page of results to return.

        page_size : int
            The number of documents per page.

        Returns
        -------
        int
            The number of documents to skip when returning the results.

        """
        return (int(page) - 1) * int(page_size)

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

        Notes
        -----
        This method needs to be implemented in derived classes.

        """
        return self.raise_method_not_implemented()

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
        |list| of |dict|
            A dictionary with keys 'count' and 'results'. The 'count'
            value is the total number of documents matching the search
            criteria. The 'results' value is a list of documents from
            the search result, with the doc ids added to each document.

        Notes
        -----
        This method needs to be implemented in derived classes.

        """
        return self.raise_method_not_implemented()

    def filter_ids(self, doc_ids, fields, value):
        """Find the ids of documents that match a value.

        Parameters
        ----------
        doc_ids : |list| of |str|
            The ids of documents to filter.

        fields : |list| of |DataField|
            |DataFields| that should be examined for a matching value.

        value : |str|
            A value used to find matching documents.

        Returns
        -------
        |list| of |str|
            The subset of ids for documents containing the given `value`
            in one or more of the specified `fields`.

        Notes
        -----
        This method needs to be implemented in derived classes.

        """
        return self.raise_method_not_implemented()

    def insert(self, doc):
        """Insert the document into the data store.

        Parameters
        ----------
        doc : dict
            A document to insert in the data store.

        Returns
        -------
        str
            The id of the inserted document.

        Notes
        -----
        This method needs to be implemented in derived classes.

        """
        return self.raise_method_not_implemented()

    def remove_by_id(self, doc_ids):
        """Remove the documents with the given ids.

        Parameters
        ----------
        doc_ids : |str| or |list| of |str|
            An id or list of ids of documents to remove from the data
            store.

        Returns
        -------
        None

        Notes
        -----
        This method needs to be implemented in derived classes.

        """
        return self.raise_method_not_implemented()
