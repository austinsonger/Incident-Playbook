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
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

# local
from cyphon.choices import FIELD_TYPE_CHOICES, TARGET_TYPE_CHOICES
from utils.validators.validators import field_name_validator

_LOGGER = logging.getLogger(__name__)


class DataFieldManager(models.Manager):
    """
    Adds methods to the default model manager.
    """

    def get_by_natural_key(self, field_name):
        """
        Allow retrieval of a DataField by its natural key instead of its
        primary key.
        """
        try:
            return self.get(field_name=field_name)
        except ObjectDoesNotExist:
            _LOGGER.error('%s "%s" does not exist',
                          self.model.__name__, field_name)


class DataField(models.Model):
    """
    Defines a field in a custom data model (Container).

    Attributes
    ----------
    field_name : str
        The name of the field in which the data will be stored.
        If the `field_type` is "ForeignKey," then the `field_name`
        also represents the primary key of an embedded |Bottle|.

    field_type : str
        The name of a Django :class:`~django.db.models.Field` subclass.

    target_type : str
        The type of target the |DataField| represents. Corresponds to a
        value in |TARGET_TYPE_CHOICES|.

    """
    field_name = models.CharField(
        max_length=40,
        unique=True,
        validators=[field_name_validator]
    )
    field_type = models.CharField(max_length=40,
                                  choices=FIELD_TYPE_CHOICES)
    target_type = models.CharField(max_length=40,
                                   choices=TARGET_TYPE_CHOICES,
                                   blank=True, null=True)

    class Meta:
        """
        Metadata options.
        """
        abstract = True
        ordering = ['field_name']

    def __str__(self):
        return "%s (%s)" % (self.field_name, self.field_type)

    def clean(self):
        super(DataField, self).clean()
        self._validate_field_type()
        self._validate_target_type()

    def _validate_field_type(self):
        """
        Returns a Boolean indicating whether the field_type is valid.
        """
        valid_field_types = [field[0] for field in FIELD_TYPE_CHOICES]
        if self.field_type is not None \
                and self.field_type not in valid_field_types:
            raise ValidationError(_('Please provide a valid field_type.'))

    def _validate_target_type(self):
        """
        Returns a Boolean indiacting whether the target_type is valid.
        """
        valid_target_types = [target[0] for target in TARGET_TYPE_CHOICES]
        if self.target_type is not None \
                and self.target_type not in valid_target_types:
            raise ValidationError(_('Please provide a valid target_type.'))

    def to_nested_datafield(self, parent_name=None):
        """Return a new |DataField| representing the current object.

        Parameters
        ----------
        parent_name : |str| or |None|
            The name of a field containing an embedded document that
            includes the field represented by current object.

        Returns
        -------
        |DataField|
            A new |DataField| instance based on the current object's
            `field_name`, `field_type` and `target_type`. If a
            `parent_name` is provided, the |DataField|'s `field_name` is
            the `parent_name` prepended to the object's `field_name`
            using dot notation.

        """
        if parent_name is not None:
            field_name = '%s.%s' % (parent_name, self.field_name)
        else:
            field_name = self.field_name

        return DataField(
            field_name=field_name,
            field_type=self.field_type,
            target_type=self.target_type,
        )

    def to_dict(self, parent_name=None):
        """Return a dict representing the object.

        Parameters
        ----------
        parent_name : |str| or |None|
            The name of a field containing an embedded document that
            includes the field represented by current object.

        Returns
        -------
        |dict|
            A |dict| containing the object's `field_name`, `field_type`,
            and `target_type`. If a `parent_name` is provided, the
            `parent_name` prepended to the object's `field_name`
            using dot notation.

        """
        if parent_name is not None:
            field_name = '%s.%s' % (parent_name, self.field_name)
        else:
            field_name = self.field_name

        field = {
            'field_name': field_name,
            'field_type': self.field_type,
            'target_type': self.target_type,
        }

        return field

    def to_key_val(self):
        """Return a key, value pair for the name and type of field.

        Returns
        -------
        |dict|
            A |dict| item mapping the object's `field_name` to its
            `field_type` and `target_type` (if any). For example,
            `{'name': 'CharField (Keyword)'`.

        """
        if self.target_type:
            target = ' (%s)' % self.target_type
        else:
            target = ''
        return {self.field_name: self.field_type + target}

