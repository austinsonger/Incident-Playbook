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
Provides DataField and Bottle classes for defining a standard data
model. These are used for displaying data in a standard format across data
sources.
"""

# standard library
from collections import OrderedDict
import json

# third party
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

# local
from cyphon.models import SelectRelatedManager, GetByNameMixin
from bottler.datafields.models import DataField, DataFieldManager
from utils.validators.validators import field_name_validator


class BottleField(DataField):
    """
    Defines a field in a custom data model (Bottle).
    """
    embedded_doc = models.ForeignKey('Bottle', blank=True, null=True)

    objects = DataFieldManager()

    def clean(self):
        super(BottleField, self).clean()

        if self.field_type == 'EmbeddedDocument' and self.embedded_doc is None:
            raise ValidationError(_('An embedded doc must be defined for an ' \
                                  + 'EmbeddedDocument field.'))

        if self.field_type != 'EmbeddedDocument' and self.embedded_doc:
            raise ValidationError(_('If an embedded doc is defined, ' \
                                  + 'the field type must be EmbeddedDocument.'))

    @property
    def embedded_doc_name(self):
        """
        Returns the name of the Bottle for an embedded document.
        """
        return self.embedded_doc.name


class BottleManager(SelectRelatedManager, GetByNameMixin):
    """
    Adds methods to the default model manager.
    """
    pass


class Bottle(models.Model):
    """
    Defines a data model for displaying data in a standard format across
    different social media platforms. Consists of a set of DataFields,
    which define the field names and types in the data model.

    The Bottle's name may be used as a field name for an embedded MongoDB
    document, so it should conform to MongoDB naming conventions for fields.
    """
    name = models.CharField(max_length=40, unique=True,
                            validators=[field_name_validator])
    fields = models.ManyToManyField(
        BottleField,
        related_name='bottles',
        related_query_name='bottle'
    )

    objects = BottleManager()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def _get_bottlefields(self, bottle_name):
        """
        Takes the primary key of a Bottle and eturns a QuerySet of its
        BottleFields.
        """
        if bottle_name is None:
            return self.fields.all()
        else:
            bottle = Bottle.objects.get_by_natural_key(bottle_name)
            return bottle.fields.all()

    @staticmethod
    def _create_key(field_name, parent_name=None):
        """
        Takes the name of a document field and, optionally, the name of a
        parent field. Returns a key to the field using dot notation.
        """
        if parent_name:
            return '%s.%s' % (parent_name, field_name)
        else:
            return field_name

    def field_exists(self, bottlefield):
        """
        Takes a BottleField and returns a Boolean indicating whether the
        field is present in the Bottle.
        """
        return self.fields.filter(pk=bottlefield.pk).exists()

    def get_fields(self, bottle_name=None, parent_name=None):
        """
        Takes the primary key of a Bottle and, optionally, a string
        representing the name of a parent Bottle. Returns a list of data
        dictionaries describing the field_name, field_type, and target_type of
        each BottleField in the Bottle. This includes any nested BottleFields
        associated with embedded Bottles (i.e., BottleFields that are
        ForeignKeys to other Bottles).
        """
        fields = []

        for bottlefield in self._get_bottlefields(bottle_name):

            # base case: not a ForeignKey
            if bottlefield.field_type != 'EmbeddedDocument':
                datafield = bottlefield.to_nested_datafield(parent_name)
                fields.append(datafield)

            # recursive case: DataField refers to a Bottle
            else:
                field_label = self._create_key(bottlefield.field_name,
                                               parent_name)
                nested_fields = self.get_fields(
                    bottle_name=bottlefield.embedded_doc_name,
                    parent_name=field_label,
                )
                fields.extend(nested_fields)

        return fields

    def get_field_choices(self, bottle_name=None, parent_name=None):
        """
        Takes the primary key of a Bottle and, optionally, a string
        representing the name of a parent Bottle. Returns a list of 2-tuples
        representing (value, label) pairs for DataFields associated with
        the Bottle. This includes any nested DataFields associated with
        embedded Bottles (i.e., DataFields that are ForeignKeys to other
        Bottles).

        Returns choices in a format suitable for use in a limit_choices_to
        argument for a ForeignKey Field in a Django Model, e.g.:

        >>> bottle.get_bottlefield_choices()
        >>> [('created_date:DateTimeField', 'created_date'),
            ('text:textCharField', 'text'),
            ('user.screen_name:CharField', 'user.screen_name'),
            ('user.profile_pic:CharField', 'user.profile_pic')]

        """
        fields = []

        for bottlefield in self._get_bottlefields(bottle_name):

            field_label = self._create_key(bottlefield.field_name, parent_name)

            # base case: not a ForeignKey or other excluded field type
            if bottlefield.field_type != 'EmbeddedDocument':
                value = '%s:%s' % (field_label, bottlefield.field_type)
                fields.append((value, field_label))

            # recursive case: DataField refers to a Bottle
            else:
                nested_fields = self.get_field_choices(
                    bottle_name=bottlefield.embedded_doc_name,
                    parent_name=field_label,
                )
                fields.extend(nested_fields)

        return fields

    def get_structure(self, bottle_name=None):
        """
        Takes a Bottle natural key and returns an OrderedDict representing
        the data model defined by the Bottle.
        """
        fields = {}

        for bottlefield in self._get_bottlefields(bottle_name):

            # base case: not a ForeignKey
            if bottlefield.field_type != 'EmbeddedDocument':
                field_info = bottlefield.to_key_val()
                fields.update(field_info)

            # recursive case: DataField refers to a Bottle
            else:
                nested_fields = self.get_structure(bottlefield.embedded_doc_name)
                fields[bottlefield.field_name] = nested_fields

        return OrderedDict(sorted(fields.items()))

    def preview(self):
        """
        Returns a JSON string representing the data model defined by
        the Bottle.
        """
        structure = self.get_structure()
        return json.dumps(structure, indent=4)

    preview.short_description = _('Bottle preview')
