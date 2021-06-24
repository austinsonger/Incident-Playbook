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
from collections import OrderedDict
import json
import logging

# third party
from django.conf import settings
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

# local
from cyphon.models import GetByNameManager
from cyphon.choices import TEXT_FIELDS
from bottler.bottles.models import Bottle
from bottler.labels.models import Label

_DISTILLERY_SETTINGS = settings.DISTILLERIES

_LOGGER = logging.getLogger(__name__)


class ContainerManager(GetByNameManager):
    """
    Adds methods to the default model manager.
    """

    def get_queryset(self):
        """
        Overrides the default get_queryset method to select the related
        Bottle and Label.
        """
        default_queryset = super(ContainerManager, self).get_queryset()
        return default_queryset.select_related()


class Container(models.Model):
    """
    Attributes:
        name: a string representing the name of the Container
        bottle: a Bottle in which to store data
        label: a Label containing metadata about the contents of a Bottle
    """
    name = models.CharField(max_length=40, unique=True)
    bottle = models.ForeignKey(Bottle, on_delete=models.PROTECT)
    label = models.ForeignKey(
        Label,
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )

    objects = ContainerManager()

    class Meta:
        ordering = ['name']
        unique_together = ('bottle', 'label')

    def __str__(self):
        return self.name

    # TODO(LH): need vaildation between label and bottle

    @cached_property
    def fields(self):
        """
        Returns
        -------
        list of DataFields

        """
        fields = []

        if self.label:
            label_fields = self.label.get_fields()
            fields.extend(label_fields)

        bottle_fields = self.bottle.get_fields()
        fields.extend(bottle_fields)

        return fields

    @property
    def field_dicts(self):
        """
        Returns a list of data dictionaries describing the field_name,
        field_type, and target_type of each BottleField and LabelField
        associated with the Container.
        """
        return [field.to_dict() for field in self.fields]

    def get_bottle_structure(self):
        """
        Returns a dictionary representing the data model defined by the
        Container's Bottle.
        """
        return self.bottle.get_structure()

    def get_label_structure(self):
        """
        Returns a dictionary representing the Container's Label.
        """
        if not self.label:  # pragma: no cover
            raise RuntimeError('Container "%s" has no Label' % self.name)
        return self.label.get_structure()

    def add_label(self, data):
        """
        Takes a dictionary of data, adds a '_metadata' field containing a
        dictionary of metadata, and returns the 'labeled' data.
        """
        if self.label:
            return self.label.add(data)
        else:
            return data

    def get_sample(self, data):
        """
        Takes a dictionary of bottled data and returns a dictionary of 'teaser'
        data.
        """
        if hasattr(self, 'taste'):
            return self.taste.get_sample(data)
        else:
            _LOGGER.warning('Container "%s" has no Taste to sample data',
                            str(self))
            return {}

    def get_blind_sample(self, data, codebook):
        """
        Takes a dictionary of bottled data and returns a dictionary of redacted
        'teaser' data, using the Distillery's CodeBook.
        """
        if hasattr(self, 'taste'):
            return self.taste.get_blind_sample(data, codebook)
        else:
            _LOGGER.warning('Container "%s" has no Taste to sample data',
                            str(self))
            return {}

    def get_taste_text_fields(self):
        """
        Returns a list of DataFields for searchable text fields
        associated with the Taste.
        """
        field_names = self.taste.get_text_fields()
        return [field for field in self.fields \
                if field.field_name in field_names]

    def get_text_fields(self):
        """
        Returns a list of DataFields for searchable text fields
        associated with the Container.
        """
        return [field for field in self.fields \
                if field.field_type in TEXT_FIELDS]

    def get_field_list(self):
        """

        """
        return [field.field_name for field in self.fields]

    def get_structure(self):
        """
        Returns an OrderedDict representing the data model defined by the
        Container.
        """
        structure = OrderedDict()

        if self.label:
            label_structure = self.get_label_structure()
            label_fields = OrderedDict(sorted(label_structure.items()))
            structure.update({_DISTILLERY_SETTINGS['LABEL_KEY']: label_fields})

        bottle_structure = self.get_bottle_structure()
        bottle_fields = OrderedDict(sorted(bottle_structure.items()))
        structure.update(bottle_fields)

        return structure

    def preview(self):
        """
        Returns a JSON string representing the Container.
        """
        structure = self.get_structure()
        return json.dumps(structure, indent=4)

    preview.short_description = _('container peview')
