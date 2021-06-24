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

"""

# standard library
import logging

# third party
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.utils.functional import cached_property

# local
from cyphon.models import SelectRelatedManager, FindEnabledMixin

_LOGGER = logging.getLogger(__name__)


class ChuteManager(SelectRelatedManager, FindEnabledMixin):
    """
    Adds methods to the default model manager.
    """

    settings = {
        'DEFAULT_CHUTE': 'default'
    }

    def get_by_natural_key(self, sieve, munger):
        """
        Allow retrieval of a DataChute by its natural key instead of its
        primary key.
        """
        try:
            return self.get(sieve=sieve, munger=munger)
        except ObjectDoesNotExist:
            _LOGGER.error('%s for sieve %s and munger %s does not exist',
                          self.model.__name__, sieve, munger)

    @property
    def _munger_model(self):
        """

        """
        return self.model._meta.get_field('munger').rel.to

    @cached_property
    def _default_munger(self):
        """
        Returns the default Chute specified in the site configuration.
        """
        default_munger_name = self.settings['DEFAULT_MUNGER']

        try:
            munger_model = self._munger_model
            return munger_model.objects.get(name=default_munger_name)
        except ObjectDoesNotExist:
            _LOGGER.error('Default %s "%s" is not configured.',
                          self._munger_model.__name__,
                          default_munger_name)

    @property
    def _default_munger_enabled(self):
        """

        """
        return self.settings['DEFAULT_MUNGER_ENABLED'] and self._default_munger

    def _process_with_default(self, doc_obj):
        """

        """
        return self._default_munger.process(doc_obj)

    def process(self, doc_obj):
        """

        """
        enabled_chutes = self.find_enabled()
        saved = False

        for chute in enabled_chutes:
            result = chute.process(doc_obj)
            if result:
                saved = True

        if not saved and self._default_munger_enabled:
            self._process_with_default(doc_obj)


class Chute(models.Model):
    """

    """
    enabled = models.BooleanField(default=True)

    class Meta:
        """
        Metadata options for a Django Model.
        """
        abstract = True
        unique_together = ('sieve', 'munger')
        ordering = ['sieve', 'munger']

    def __str__(self):
        if self.sieve:
            return '%s -> %s' % (self.sieve, self.munger)
        else:
            return '-> %s' % self.munger

    def _is_match(self, data):
        """
        Takes a data dictionary and returns True if the dictionary
        matches the rules defined by the Chute's sieve. Otherwise,
        returns False.
        """
        if self.sieve:
            return self.sieve.is_match(data)
        else:
            return True

    def _munge(self, doc_obj):
        """
        Takes a DocumentObj, processes the data with the Chute's munger,
        and returns the document id of the distilled document.
        """
        return self.munger.process(doc_obj)

    def process(self, doc_obj):
        """
        Takes a DocumentObj and determines if the data is a match for
        the Chute's sieve. If it is, processes the data with the Chute's
        munger and returns the document id of the distilled document.
        Otherwise, returns None.
        """
        if self.enabled and self._is_match(doc_obj.data):
            return self._munge(doc_obj)

    def thread_process(self, queue, **kwargs):
        """
        Takes a Queue, a data dictionary, a document id, and a string
        indicating the source of the data. Determines if the data is a
        match for the Chute's sieve. If it is, processes the data with
        the Chute's munger and returns the document id of the distilled
        document. Otherwise, returns None.
        """
        result = self.process(**kwargs)
        if result is not None:
            queue.put(True)
