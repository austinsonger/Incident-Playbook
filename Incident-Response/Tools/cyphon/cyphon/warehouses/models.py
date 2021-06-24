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
This module defines models and model managers for storing and retrieving data.

These models provide a layer of abstraction between Cyphon and the
storage engines with which it interacts.

===========================  ==================================================
Class                        Description
===========================  ==================================================
:class:`~Collection`         A document collection, doctype, or database table.
:class:`~CollectionManager`  Model manager for |Collections|.
:class:`~Warehouse`          A database or search index.
:class:`~WarehouseManager`   Model manager for |Warehouses|.
===========================  ==================================================

"""

# standard library
import importlib
import logging

# third party
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

# local
from engines.registry import ENGINES_PACKAGE, ENGINE_MODULE, BACKEND_CHOICES
from utils.validators.validators import db_name_validator, lowercase_validator

_PAGE_SIZE = settings.PAGE_SIZE
_WAREHOUSE_SETTINGS = settings.WAREHOUSES

_LOGGER = logging.getLogger(__name__)


class WarehouseManager(models.Manager):
    """Manage |Warehouse| objects.

    Adds methods to the default Django model manager.
    """

    def get_by_natural_key(self, backend, name):
        """Get a |Warehouse| by its natural key.

        Allows retrieval of a |Warehouse| by its natural key instead of
        its primary key.

        Parameters
        ----------
        backend : str
            The backend of the |Warehouse|.

        name : str
            The name of the |Warehouse|.

        Returns
        -------
        |Warehouse|
            The |Warehouse| associated with the natural key.

        """
        try:
            return self.get(backend=backend, name=name)
        except ObjectDoesNotExist:
            _LOGGER.error('%s %s.%s does not exist',
                          self.model.__name__, backend, name)


class Warehouse(models.Model):
    """Define a database or search index.

    Attributes
    ----------
    backend : str
        Lowercase name of a storage engine, such as 'elasticsearch'.
        This corresponds to the base file name of the module containing
        the |Engine| subclass for that storage engine. Choices are
        constrained to |BACKEND_CHOICES|.

    name : str
        The name of a database or search index.

    time_series : bool
        Whether data should be stored as a time series (e.g.,
        timestamped indexes).

    """
    _DEFAULT_STORAGE_ENGINE = _WAREHOUSE_SETTINGS['DEFAULT_STORAGE_ENGINE']

    backend = models.CharField(max_length=40, choices=BACKEND_CHOICES,
                               default=_DEFAULT_STORAGE_ENGINE.lower())
    name = models.CharField(
        max_length=40,
        validators=[db_name_validator, lowercase_validator]
    )
    time_series = models.BooleanField(
        default=False,
        help_text=_('When used with Elasticsearch, stores each day\'s '
                    'data in a separate index. Allows easy deletion '
                    'of old data in Elasticsearch.'))

    objects = WarehouseManager()

    class Meta(object):
        """Metadata options."""

        unique_together = ('backend', 'name')
        ordering = ['name']

    def __str__(self):
        """Get a string representation of the Warehouse instance.

        Returns a printable string showing the `backend` and `name`.
        """
        return '%s.%s' % (self.backend, self.name)

    def _allow_time_series(self):
        """Whether data can be stored in a time series.

        Returns a `bool` indicating whether the backend can store data
        in a time series (e.g., timestamped indexes).
        """
        module = self.get_module()
        return module.TIME_SERIES_ENABLED

    def clean(self):
        """Validate the model as a whole.

        Provides custom model validation. If `time_series` is |True|,
        checks that the backend can work with a time series.

        Returns
        -------
        None

        Raises
        ------
        ValidationError
            If `time_series` is |True| but the selected `backend`
            cannot work with a time series, or if any default Django
            model validations fail.

        See also
        --------
        See Django's documentation for the
        :meth:`~django.db.models.Model.clean` method.

        """
        super(Warehouse, self).clean()
        if self.time_series and not self._allow_time_series():
            raise ValidationError(_('The time series feature is not '
                                    'enabled for the selected backend.'))

    def get_module(self):
        """Get the module for interacting with the backend.

        Returns
        -------
        :class:`~module`
            The module that contains the |Engine| subclass for
            interacting with the Warehouse's backend.

        """
        # e.g., 'engines.mongodb.engine'
        module_full_name = '%s.%s.%s' % (ENGINES_PACKAGE, self.backend,
                                         ENGINE_MODULE)

        # load the module (will raise ImportError if module cannot be loaded)
        module = importlib.import_module(module_full_name)
        return module


class CollectionManager(models.Manager):
    """Manage |Collection| objects.

    Customizes the default Django model manager by adding and overriding
    methods.
    """

    def get_queryset(self):
        """Get the initial |Collection| queryset.

        Overrides the default `get_queryset` method to also select
        related |Warehouses|.

        Returns
        -------
        |Queryset|
            A |Queryset| of |Collections|.

        See also
        --------
        Django's documentation contains instructions on how to
        `select related`_ objects and `modify an initial queryset`_.

        """
        default_queryset = super(CollectionManager, self).get_queryset()
        return default_queryset.select_related('warehouse')

    def get_by_natural_key(self, backend, database, name):
        """Get a |Collection| by its natural key.

        Allows retrieval of a |Collection| by its natural key instead of its
        primary key.

        Parameters
        ----------
        backend : str
            The backend of the |Warehouse| to which the |Collection| belongs.

        database : str
            The name of the |Warehouse| to which the |Collection| belongs.

        name : str
            The name of the |Collection|.

        Returns
        -------
        |Collection|
            The |Collection| associated with the natural key.

        """
        warehouse = Warehouse.objects.get_by_natural_key(backend, database)
        try:
            return self.get(warehouse=warehouse, name=name)
        except ObjectDoesNotExist:
            _LOGGER.error('%s %s.%s.%s does not exist',
                          self.model.__name__, backend, database, name)


class Collection(models.Model):
    """Define a document collection, document type, or database table.

    Attributes
    ----------
    warehouse : Warehouse
        The |Warehouse| in which the |Collection| resides.

    name : str
        The name of a document collection, doc type, or database table,
        depending on the |Warehouse| backend.

    """

    warehouse = models.ForeignKey(Warehouse, related_name='collections',
                                  related_query_name='collection')
    name = models.CharField(max_length=40, verbose_name='collection name',
                            validators=[db_name_validator])

    objects = CollectionManager()

    class Meta(object):
        """Metadata options."""

        unique_together = ('warehouse', 'name')
        ordering = ['warehouse', 'name']

    def __str__(self):
        """Get a string representation of the Collection instance.

        Returns a printable string showing the `backend` and `name` of
        the Collection's |Warehouse|, as well as the Collection's `name`.
        """
        return '%s.%s.%s' % (self.warehouse.backend, self.warehouse.name,
                             self.name)

    @cached_property
    def company(self):
        """The |Company| associated with the Collection.

        Returns
        -------
        |Company|
            The |Company| associated with the Collection's |Distillery|.

        """
        try:
            return self.distillery.company
        except ObjectDoesNotExist:
            return None

    def get_company(self):
        """Get the |Company| associated with the Collection.

        This method is used to display the Company in the admin list view.

        Returns
        -------
        |Company|
            The |Company| associated with the Collection's |Distillery|.

        """
        return self.company

    get_company.short_description = 'company'

    def _get_module(self):
        """Get the `engines` module for working with the Collection.

        Returns the module that contains the |Engine| suclass for
        interacting with the Collection.
        """
        return self.warehouse.get_module()

    def _get_class(self):
        """Get the |Engine| subclass for working with the Collection.

        Returns the |Engine| suclass responsible for communicating with
        the backend. This will raise an :exc:`~AttributeError` if the
        class cannot be found.
        """
        module = self._get_module()
        return getattr(module, module.ENGINE_CLASS)

    def get_backend(self):
        """Get the backend used by the Collection.

        Returns the name of the backend associated with the Collection's
        |Warehouse|. This method can be used to display the backend in
        the admin list view.

        Returns
        -------
        str
            The backend used by the Collection's |Warehouse|.

        """
        return self.warehouse.backend

    get_backend.short_description = 'backend'

    def in_time_series(self):
        """Whether the Collection's |Warehouse| is a time series.

        Returns a |bool| indicating whether the Collection's |Warehouse|
        stores data in a time series (e.g., timestamped indexes).

        Returns
        -------
        bool
            Whether data is stored as a time series.

        """
        return self.warehouse.time_series

    in_time_series.short_description = 'time series'

    def get_warehouse_name(self):
        """Get the name of the Collection's |Warehouse|.

        This method is used to display the Warehouse name in the admin
        list view.

        Returns
        -------
        str
            The name of the Collection's |Warehouse|.

        """
        return self.warehouse.name

    get_warehouse_name.short_description = 'warehouse name'

    def get_schema(self):
        """Get the |DataFields| used by documents in the Collection.

        Returns
        -------
        |list| of |DataFields|
            The |DataFields| in the |Container| used by the Collection's
            |Distillery|.

        """
        if hasattr(self, 'distillery'):
            return self.distillery.schema
        else:
            return []

    def get_sample(self, doc):
        """Get a teaser for a doc.

        Parameters
        ----------
        doc : dict
            A document that conforms to the Collection's schema, which
            is defined by the |Container| used by the Collection's
            |Distillery|.

        Returns
        -------
        dict
            A teaser for the original the `doc`.

        """
        return self.distillery.get_sample(doc)

    def _get_engine(self):
        """Get an |Engine| for handling documents.

        Returns an instance of an |Engine| subclass that can be used to
        handle documents associated with the Collection.

        This method is used to simplify testing, since it can be called
        in different contexts after the Collection is intialized
        (whereas the `engine` property that uses it is cached, making
        patches more difficult to apply).
        """
        engine_class = self._get_class()
        try:
            return engine_class(self)
        except ConnectionRefusedError as error:
            _LOGGER.error(error)

    @cached_property
    def engine(self):
        """An |Engine| for handling documents.

        Returns
        -------
        |Engine|
            An instance of an |Engine| subclass that can be used to
            handle documents associated with the Collection.

        """
        return self._get_engine()

    def find_by_id(self, doc_ids):
        """Find one or more documents by id.

        Parameters
        ----------
        doc_ids : |str| or |list| of |str|
            A document id or a list of document ids.

        Returns
        -------
        |dict|, |list| of |dict|, or |None|
            Documents that match the given id(s). Returns a |list| of
            documents if `doc_ids` is a |list|; otherwise returns a
            single document. If no matches are found, returns |None|.

        """
        return self.engine.find_by_id(doc_ids)

    def find(self, query, sorter=None, page=1, page_size=_PAGE_SIZE):
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
        return self.engine.find(query, sorter, page, page_size)

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

        """
        return self.engine.filter_ids(doc_ids, fields, value)

    def insert(self, doc):
        """Save a document to the Collection.

        Parameters
        ----------
        doc : dict
            A document to insert into the data store represented by the
            Collection.

        Returns
        -------
        str
            The id of the inserted document.

        """
        try:
            return self.engine.insert(doc)

        # different backends may throw different exceptions
        except Exception as error:  # pylint: disable=W0703
            _LOGGER.exception('Insertion error: %s', error)

    def remove_by_id(self, doc_ids):
        """Remove the documents with the given ids.

        Parameters
        ----------
        doc_ids : |str| or |list| of |str|
            An id or list of ids of documents to remove from the
            Collection.

        Returns
        -------
        None

        """
        return self.engine.remove_by_id(doc_ids)
