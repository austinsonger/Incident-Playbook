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
import copy
import json

# third party
from django.conf import settings
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.translation import ugettext_lazy as _

# local
from cyphon.models import GetByNameManager
from bottler.datafields.models import DataField, DataFieldManager

_DISTILLERY_SETTINGS = settings.DISTILLERIES


class LabelField(DataField):
    """
    Defines a field in a Label.

    Assigns a Procedure or Inspection to a Bottle to allow data enhancements
    for bottled data.

    """
    PROCEDURE = models.Q(app_label='procedures', model='procedure')
    INSPECTION = models.Q(app_label='inspections', model='inspection')
    CONTENT_TYPES = PROCEDURE | INSPECTION

    content_type = models.ForeignKey(
        ContentType,
        limit_choices_to=CONTENT_TYPES,
        verbose_name=_('analyzer type'),
        help_text=_('Inspections determine whether data match a set of rules, '
                    'defined by regular expressions. <br>Procedures perform more '
                    'complex analyses, such as sentiment analysis or '
                    'geolocation.')
    )
    object_id = models.PositiveIntegerField(
        verbose_name=_('analyzer id'),
        help_text=_('The id of the inspection or procedure that will '
                    'analyze the data.')
    )
    analyzer = GenericForeignKey()

    objects = DataFieldManager()

    class Meta:
        """
        Metadata options.
        """
        unique_together = ('field_name', 'content_type', 'object_id')

    def __str__(self):
        return "%s:%s <- %s (%s)" % (self.field_name, self.field_type,
                                     self.analyzer, self.analyzer_type)

    @property
    def analyzer_type(self):
        """
        Returns the name of the class for the type of analyzer, which can be
        either an Inspection or a Procedure.
        """
        return self.content_type.model

    def _get_result(self, data):
        """
        Takes a data dictionary of bottled data and returns the result of the
        the analysis performed by the Analyzer's Procedure or Inspection.

        This method requires that both Inspections and Procedures
        have a method with this name.
        """
        return self.analyzer.get_result(data)

    def create(self, data):
        """
        Takes a dictionary of bottled data and returns a dictionary object
        containing the result of the analysis.
        """
        key = self.field_name
        value = self._get_result(data)
        return {key: value}


class LabelManager(GetByNameManager):
    """
    Adds methods to the default model manager.
    """

    def get_queryset(self):
        """
        Overrides the default get_queryset method to select the related
        BottleFields.
        """
        default_queryset = super(LabelManager, self).get_queryset()
        return default_queryset.prefetch_related('fields')


class Label(models.Model):
    """
    A Label defines a collection of LabelFields used to analyze and add
    metadata to a dictionary of bottled data.
    """
    name = models.CharField(max_length=40, unique=True)
    fields = models.ManyToManyField(LabelField)

    objects = LabelManager()

    def __str__(self):
        return self.name

    def create(self, data):
        """
        Takes a dictionary of bottled data and returns a dictionary of metadata
        containing the results of analyses for the Label's LabelFields.
        """
        label = {}

        for field in self.fields.all():
            item = field.create(data)
            label.update(item)

        return {_DISTILLERY_SETTINGS['LABEL_KEY']: label}

    def add(self, data):
        """
        Takes a dictionary of bottled data and returns the dictionary updated
        with metadata containing the results of analyses for the Label's
        fields.
        """
        data_copy = copy.deepcopy(data)
        label = self.create(data_copy)
        data_copy.update(label)
        return data_copy

    def get_fields(self):
        """
        Returns a list of data dictionaries containing the field_name,
        field_type, and target_type of each of the Label's fields.
        """
        fields = []

        for field in self.fields.all():
            label_key = _DISTILLERY_SETTINGS['LABEL_KEY']
            nested_datafield = field.to_nested_datafield(label_key)
            fields.append(nested_datafield)

        return fields

    def get_structure(self):
        """
        Returns an OrderedDict representing the Label.
        """
        fields = {}

        for labelfield in self.fields.all():
            field_info = labelfield.to_key_val()
            fields.update(field_info)

        return OrderedDict(sorted(fields.items()))

    def preview(self):
        """
        Returns a JSON string representing the Label.
        """
        structure = self.get_structure()
        return json.dumps(structure, indent=4)

    preview.short_description = _('label preview')
