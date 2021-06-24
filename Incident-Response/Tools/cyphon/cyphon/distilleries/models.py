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
Defines a model for storing, retrieving, and displaying documents.

===========================  ================================================
Class                        Description
===========================  ================================================
:class:`~Distillery`         Coordinates doc storage, retrieval, and display.
:class:`~DistilleryManager`  Model manager for |Distilleries|.
===========================  ================================================

"""

# standard library
import logging

# third party
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

# local
from categories.models import Category
from companies.models import Company
from cyphon.documents import DocumentObj
from cyphon.models import GetByNameMixin, SelectRelatedManager
from bottler.containers.models import Container
from distilleries import signals
from utils.dateutils.dateutils import parse_date
from warehouses.models import Collection

_DISTILLERY_SETTINGS = settings.DISTILLERIES
_PAGE_SIZE = settings.PAGE_SIZE

_LOGGER = logging.getLogger(__name__)


class DistilleryManager(SelectRelatedManager, GetByNameMixin):
    """Manage |Distillery| objects.

    Adds methods to the default Django model manager.
    """

    def get_by_collection_nk(self, backend, warehouse_name, collection_name):
        """Get a |Distillery| by the natural key of its |Collection|.

        Parameters
        ----------
        backend : str
            The backend of the |Warehouse| to which the Distillery's
            |Collection| belongs.

        warehouse_name : str
            The name of the |Warehouse| to which the Distillery's
            |Collection| belongs.

        collection_name : str
            The name of the Distillery's |Collection|.

        Returns
        -------
        |Distillery|
            The |Distillery| associated with the natural key.

        """
        collection_key = [backend, warehouse_name, collection_name]
        collection = Collection.objects.get_by_natural_key(*collection_key)
        if collection:
            return self.get(collection=collection.pk)
        else:
            _LOGGER.error('%s for Collection %s.%s.%s does not exist',
                          self.model.__name__, backend, warehouse_name,
                          collection_name)

    def have_alerts(self, queryset=None):
        """Get |Distilleries| that are associated with |Alerts|.

        Returns
        -------
        |Queryset|
            A |Queryset| of |Distilleries| that are associated with
            |Alerts|.
        """
        if queryset is None:
            queryset = self.get_queryset()
        annotated_qs = queryset.annotate(alert_cnt=models.Count('alerts'))
        return annotated_qs.filter(alert_cnt__gt=0)


class Distillery(models.Model):
    """Coordinate the storage, retrieval, and display of documents.

    Specifies the data model for a set of documents, the location where
    they are stored, and some general info about them. A Distillery can
    also construct document teasers and redact those teasers prior to
    display.

    Attributes
    ----------
    collection : Collection
        The |Collection| in which data is stored.

    container : Container
        The |Container| used to model the data.

    company : Company
        The |Company| associated with the data.

    categories : `QuerySet` of `Categories`
        A |QuerySet| of |Categories| that characterize the data.

    is_shell : bool
        Whether the Distillery is only used to model and retrieve data,
        and is not responsible for saving data. This may be the case
        if the data is saved by `Logstash`_ rather tha Cyphon.

    """

    _DATE_KEY = _DISTILLERY_SETTINGS['DATE_KEY']

    name = models.CharField(
        max_length=255,
        unique=True
    )
    collection = models.OneToOneField(
        Collection,
        primary_key=True,
        help_text=_('Storage location')
    )
    container = models.ForeignKey(
        Container,
        related_name='distilleries',
        related_query_name='distillery',
        help_text=_('Data model')
    )
    company = models.ForeignKey(Company, blank=True, null=True)
    categories = models.ManyToManyField(
        Category,
        related_name='distilleries',
        related_query_name='distillery',
        blank=True,
        help_text=_('Employ Watchdogs with these Categories.')
    )
    is_shell = models.BooleanField(
        default=False,
        help_text=_('A "shell" models and retrieves data, '
                    'but is not responsible for saving data.')
    )

    objects = DistilleryManager()

    class Meta(object):
        """Metadata options."""

        verbose_name_plural = 'distilleries'
        ordering = ['name']

    def __str__(self):
        """Get a string representation of the Distillery instance.

        Returns a printable string showing the Distillery's |Collection|.
        """
        return str(self.collection)

    @cached_property
    def codebook(self):
        """A |CodeBook| for redacting data.

        Returns
        -------
        |CodeBook|
            The |CodeBook| associated with the Distillery's |Company|.

        """
        if hasattr(self.company, 'codebook'):
            return self.company.codebook

    def _add_distillery_info(self, doc):
        """Add the Distillery's pk to a document.

        Takes a dictionary of data, adds a field containing the primary
        key of the Distillery, and returns the updated dictionary. This
        field helps identify the origin of a record in queries that
        aggregate data across |Collections|.
        """
        doc[_DISTILLERY_SETTINGS['DISTILLERY_KEY']] = self.pk
        return doc

    def _add_date(self, doc):
        """Add the current datetime to a document.

        Takes a dictionary of data, adds a field containing a |datetime|
        for the current time, and returns the updated dictionary.
        """
        doc[self._DATE_KEY] = timezone.now()
        return doc

    @staticmethod
    def _add_raw_data_info(doc, raw_doc_obj):
        """Add a reference to the location of raw data.

        Takes a dictionary of distilled data, the doc id of the original
        (undistilled) data, and a string representation of the |Collection|
        where the original data resides. Adds a location reference for the
        undistilled data to the distilled doc, and returns the updated doc.
        """
        location_ref = raw_doc_obj.location_ref
        if location_ref:
            doc[_DISTILLERY_SETTINGS['RAW_DATA_KEY']] = location_ref
        return doc

    @staticmethod
    def _add_platform_info(doc, platform):
        """Add |Platform| info to a doc.

        Takes a document and a string representation of the |Platform|
        from which the data came. Adds a field with the Platform info
        and returns the updated doc.
        """
        platform_key = _DISTILLERY_SETTINGS['PLATFORM_KEY']
        doc[platform_key] = str(platform)
        return doc

    def _add_label(self, doc):
        """Enhance a doc with metadata.

        Takes a dictionary of data, adds a '_metadata' field containing a
        dictionary of metadata, and returns the 'labeled' data.
        """
        return self.container.add_label(doc)

    def _create_doc_obj(self, doc, doc_id):
        """
        Takes a data dictionary and a document id for a document in the
        Distillery, and returns a DocumentObj for the document.
        """
        return DocumentObj(data=doc, doc_id=doc_id, collection=str(self))

    def _save_and_send_signal(self, doc):
        """Save a doc and send a |document_saved| signal.

        Takes a dictionary of data, saves it in the Distillery's
        |Collection|, and sends a signal that the document has been
        saved. This signal is received by |Alarms|, such as |Watchdogs|
        and |Monitors|.
        """
        doc_id = self.collection.insert(doc)
        doc_obj = self._create_doc_obj(doc, doc_id)
        signals.document_saved.send(sender=type(self), doc_obj=doc_obj)
        return doc_id

    def _get_date_saved_field(self):
        """Get the field containing the date when a document was saved.

        Returns the name of the field that stores the date when a
        document was saved by Cyphon.
        """
        if not self.is_shell:
            return self._DATE_KEY

    def get_bottle(self):
        """Get the |Bottle| used by the Distillery.

        Returns
        -------
        |Bottle|
            The |Bottle| associated with the Distillery's |Container|.

        """
        return self.container.bottle

    def get_backend(self):
        """Get the name of the storage engine used by the Distillery.

        Returns
        -------
        str
            The name of the storage engine associated with the
            Distillery's |Collection| (e.g., 'elasticsearch').

        """
        return self.collection.get_backend()

    def get_warehouse_name(self):
        """Get the name of the |Warehouse| used by the Distillery.

        Returns
        -------
        str
            The name of the |Warehouse| associated with the Distillery's
            |Collection|.

        """
        return self.collection.get_warehouse_name()

    def get_collection_name(self):
        """Get the name of the Distillery's |Collection|.

        Returns
        -------
        str
            The name of the |Collection| where the Distillery stores data.

        """
        return self.collection.name

    @cached_property
    def engine(self):
        """The |Engine| associated with the Distillery.

        Returns
        -------
        |Engine|
            The |Engine| that services the Distillery's |Collection|.

        """
        return self.collection.engine

    @cached_property
    def warehouse(self):
        """The |Warehouse| used by the Distillery.

        Returns
        -------
        |Warehouse|
            The |Warehouse| where the Distillery's |Collection| is located.

        """
        return self.collection.warehouse

    @cached_property
    def schema(self):
        """Get the |DataFields| in documents handled by the Distillery.

        Returns
        -------
        |list| of |DataFields|
            |DataFields| in the Distillery's |Container|.

        """
        return self.container.fields

    def get_text_fields(self):
        """Get |DataFields| that can be searched as text.

        Returns
        -------
        |list| of |DataFields|
            |DataFields| in the Distillery's |Container| that can be
            searched as text.

        """
        return self.container.get_text_fields()

    def get_field_list(self):
        """Get the names of fields in docs handled by the Distillery.

        Returns
        -------
        |list| of |str|
            Field names associated with the Distillery's |Container|.

        """
        return self.container.get_field_list()

    def find(self, query, sorter=None, page=1, page_size=_PAGE_SIZE):
        """Find documents matching a query.

        Parameters
        ----------
        query : |EngineQuery|
            An |EngineQuery| defining critieria for matching documents
            in the Distillery's |Collection|.

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
        return self.collection.find(query, sorter, page, page_size)

    def find_by_id(self, doc_ids):
        """Find one or more documents by id.

        Parameters
        ----------
        doc_ids : |str| or |list| of |str|
            A document id or a list of document ids.

        Returns
        -------
        |dict|, |list| of |dict|, or |None|
            Documents in the Distillery's |Collection| that match the
            given id(s). Returns a |list| of documents if `doc_ids` is
            a |list|; otherwise returns a single document. If no matches
            are found, returns |None|.

        """
        return self.collection.find_by_id(doc_ids)

    def filter_ids_by_content(self, doc_ids, value):
        """Find the ids of documents with text that matches a value.

        Parameters
        ----------
        doc_ids : |list| of |str|
            The ids of documents to filter.

        value : |str|
            A value used to find matching documents.

        Returns
        -------
        |list| of |str|
            The subset of ids for documents containing the given `value`
            in one or more of its text-searchable fields.

        """
        fields = self.container.get_text_fields()
        return self.collection.filter_ids(doc_ids, fields, value)

    @cached_property
    def taste(self):
        """A |Taste| for sampling the Distillery's documents.

        Returns
        -------
        |Taste| or |None|
            The |Taste| associated with the Distillery's |Container|,
            if it has one. Otherwise, returns |None|.

        """
        if hasattr(self.container, 'taste'):
            return self.container.taste

    def get_searchable_date_field(self):
        """Get the name of a searchable document date field.

        Finds the name of a |DataField| in the Distillery's |Container|
        that can be used to filter documents by date. This must be a
        DateTimeField, not merely a CharField containing a date string
        (since CharFields can't be indexed and searched as dates).

        The method will first attempt to return the
        :attr:`tastes.models.Taste.datetime` of the Distillery's
        :attr:`~Distillery.taste`. If that fails and
        :attr:`~Distillery.is_shell` is |False| (indicating that
        documents are saved by Cyphon), it will instead return the field
        that Cyphon uses to store the time when a document is saved.

        Returns
        -------
        |str| or |None|
            The name of the |DataField| in the Distillery's |Container|
            that is used to filter documents by date. Returns |None| if
            no such field exists.

        """
        if self.taste and self.taste.datetime:
            return self.taste.datetime
        else:
            return self._get_date_saved_field()

    def get_date_field(self):
        """Get the name of the document date field.

        Finds the name of the |DataField| in the Distillery's |Container|
        that represents the document's date.

        The method will first attempt to return the date field defined
        by the Distillery's :attr:`~Distillery.taste`, which can be
        either a DateTimeField or a CharField. If that fails and
        :attr:`~Distillery.is_shell` is |False| (indicating that
        documents are saved by Cyphon), it will instead return the field
        that Cyphon uses to store the time when a document is saved.

        Returns
        -------
        |str| or |None|
            The name of the |DataField| in the Distillery's |Container|
            that stores the date associated with a document. Returns
            |None| if no such field exists.

        Warning
        -------
        This method is used to find the name of the date field in a
        document, without regard to field type (which could be
        'CharField'). Thus, it will not necessarily return a field
        that can actually be searched as a date. For that use case,
        try the :meth:`~Distillery.get_searchable_date_field` method.

        """
        if self.taste:
            date_field = self.taste.get_date_field()
            if date_field:
                return date_field

        return self._get_date_saved_field()

    def _get_taste_date(self, doc):
        """Get the date from a document's teaser.

        Takes a document and returns a |datetime| for it, as defined by
        the Distillery's |Taste|, if it has one. Otherwise, returns |None|.
        """
        if self.taste:
            return self.taste.get_date(doc)

    def get_date(self, doc):
        """Get the |datetime| associated with a document.

        Attempts to return the date defined by the Distillery's |Taste|.
        If none exists, attempts to return the date when the Distillery
        saved the data.

        Parameters
        ----------
        doc : dict
            A document in the Distillery's |Collection|.

        Returns
        -------
        |datetime| or |None|
            The date associated with the document, if one exists.
            Otherwise, returns |None|.

        Warning
        -------
        If the Distillery is only used to retrieve documents saved by
        other means (e.g., Logstash), the document will not contain the
        '_saved_date' field that Cyphon adds to saved documents. In this
        case, `get_date()` will return |None| if no date is defined
        by the Distillery's |Taste|.

        """
        taste_date = self._get_taste_date(doc)
        if taste_date:
            return taste_date
        else:
            date = doc.get(self._DATE_KEY)
            return parse_date(date)

    def get_sample(self, doc):
        """Get a teaser for a document.

        Returns
        -------
        dict
             A teaser for the document.

        """
        return self.container.get_sample(doc)

    def get_blind_sample(self, doc):
        """Get a redacted teaser for a document.

        Creates a redacted teaser for a document, using the Distillery's
        |Taste| and |CodeBook|.

        Parameters
        ----------
        doc : dict

        Returns
        -------
        dict
            A redacted teaser for the document.

        """
        if self.codebook:
            return self.container.get_blind_sample(doc, self.codebook)
        else:
            return self.container.get_sample(doc)

    def save_data(self, doc_obj):
        """Save a document to the Distillery's |Collection|.

        Takes a document from a DocumentObj, updates it with a reference to
        the location of the original data, and saves the new document to
        the Distillery's |Collection|.

        Parameters
        ----------
        doc_obj : |DocumentObj|
            A document to be saved.

        Returns
        -------
        str
            The id of the saved document.

        """
        doc = self._add_date(doc_obj.data)
        doc = self._add_distillery_info(doc)
        if doc_obj.doc_id and doc_obj.collection:
            doc = self._add_raw_data_info(doc, doc_obj)
        if doc_obj.platform:
            doc = self._add_platform_info(doc, doc_obj.platform)
        doc = self._add_label(doc)
        doc_id = self._save_and_send_signal(doc)
        return doc_id
