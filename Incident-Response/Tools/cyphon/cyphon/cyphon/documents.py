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
Defines a |QueryFieldset| class. |QueryFieldsets| are used to construct
queries to data stores.
"""

# standard library
import logging

# third party
from django.apps import apps
from django.conf import settings
from django.utils.functional import cached_property

_DISTILLERY_SETTINGS = settings.DISTILLERIES

_LOGGER = logging.getLogger(__name__)


class DocumentObj(object):
    """

    Attributes
    ----------
    data : `str`, `dict`, or `email.message.Message`
        The document data.

    doc_id : str
        The unique id (primary key) for the document.

    collection : str
        A string representation of the |Collection| in which the
        document is stored (e.g., 'elasticsearch.cyphon.syslog').

    platform : str
        The platform from which the data was gathered (e.g., 'twitter').

    """

    def __init__(self, data=None, doc_id=None, collection=None, platform=None):
        self.data = data
        self.doc_id = doc_id
        self.collection = collection
        self.platform = platform

    def __str__(self):
        return "%s:%s" % (self.collection, self.doc_id)

    def _get_distillery_natural_key(self):
        """Get the natural key for the document's Distillery.

        Returns a 3-item list containing the names of the backend,
        Warehouse, and Collection associated with the document.
        """
        if self.collection:
            return self.collection.split('.')

    @property
    def location_ref(self):
        """Create a location reference for a doc.

        Takes a document id and a string representing a |Collection|.
        Returns a dictionary that breaks down the location of the
        document so it can be easily located.
        """
        try:
            natural_key = self._get_distillery_natural_key()

            return {
                _DISTILLERY_SETTINGS['BACKEND_KEY']: natural_key[0],
                _DISTILLERY_SETTINGS['WAREHOUSE_KEY']: natural_key[1],
                _DISTILLERY_SETTINGS['COLLECTION_KEY']: natural_key[2],
                _DISTILLERY_SETTINGS['DOC_ID_KEY']: self.doc_id
            }
        except (AttributeError, IndexError, TypeError):
            _LOGGER.error('Info for raw data document %s could not be added',
                          self)

    @cached_property
    def distillery(self):
        """The |Distillery| associated with the DocumentObj.

        Returns
        -------
        |Distillery| or |None|
            The |Distillery| associated with the document, if it exists.

        """
        natural_key = self._get_distillery_natural_key()
        try:
            # use get_model to avoid circular dependency
            distillery_model = apps.get_model('distilleries', 'Distillery')
            return distillery_model.objects.get_by_collection_nk(*natural_key)
        except AttributeError:
            _LOGGER.error('The DocumentObj %s has an improperly formatted '
                          'Collection string', self)
