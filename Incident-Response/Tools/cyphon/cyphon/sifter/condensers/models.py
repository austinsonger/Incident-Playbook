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
Provides abstract classes for defining a crosswalk between a custom data model and
a model used by an external data platform, such as Twitter.

The crosswalk allows data from a Pipe to be saved in a user-defined format
(i.e., a Bottle).
"""

# standard library
import logging

# third party
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

# local
from bottler.bottles.models import Bottle, BottleField
from parsers.models import Parser

LOGGER = logging.getLogger(__name__)


class Condenser(models.Model):
    """
    Defines a crosswalk for transforming data into a user-defined format defined
    by a custom Bottle.

    A Condenser is composed of Fittings between the fields in a Bottle object
    and the fields in an object returned by a Pipe or a Chute.
    """
    name = models.CharField(
        max_length=40,
        unique=True,
        help_text=_('It\'s a good idea to name condensers after the type of '
                    'data they are condensing, e.g., "email," "tweet," etc.')
    )
    bottle = models.ForeignKey(
        Bottle,
        help_text=_('The bottle (custom data  model) into which the raw data '
                    'will be distilled and stored.')
    )

    class Meta(object):
        """Metadata options."""

        abstract = True
        ordering = ['name']

    def __str__(self):
        return self.name

    def field_is_in_bottle(self, bottlefield):
        """
        Takes a BottleField and returns a Boolean indicating whether the
        field is present in the Bottle associated with the chosen Condenser.
        """
        return self.bottle.field_exists(bottlefield)

    # def process(self, data):
    #     """
    #     Takes a dictionary of data and returns a dictionary that distills the
    #     data using the crosswalk defined by the Condenser.
    #     """
    #     custom_doc = {}
    #     for fitting in self.fittings.all():
    #         custom_doc[fitting.target_field_name] = fitting.process(data)

    #     return custom_doc

    def _condense(self, data, condenser, **kwargs):
        """
        Takes a dictionary of data (e.g., of a social media post) and a
        Condenser. Returns a dictionary that distills the data
        using the crosswalk defined by the Condenser.
        """
        custom_doc = {}

        for fitting in condenser.fittings.all():

            if fitting.is_parser():
                value = fitting.process(data=data, **kwargs)
                custom_doc[fitting.target_field_name] = value

            # if the field represents another Bottle, use recursion
            else:
                condenser = fitting.field_parser
                custom_doc[fitting.target_field_name] = self._condense(
                    data=data, condenser=condenser, **kwargs)

        return custom_doc

    def process(self, data, **kwargs):
        """
        Takes a dictionary of data (e.g., of a social media post) and a
        Condenser. Returns a dictionary that distills the data
        using the crosswalk defined by the Condenser.
        """
        return self._condense(data=data, condenser=self, **kwargs)


class Fitting(models.Model):
    """
    Defines a mapping between a BottleField and a field in an object returned by
    a Pipe or a Chute.

    Attributes:
        target_field: the BottleField into which the value will be saved
        object_id: the primary key of the Parser or Condenser
        field_parser: a Parser or Condenser associated with the Fitting

    Implement in subclasses:
        content_type: the ContentType associated with the Fitting, which can
            either be a Parser or a Condenser (for an EmbeddedDocument)


    Derived classes should also implement a condenser attribute, which specifies
    the Condenser to which the Fitting belongs.

    """
    CONTENT_TYPES = None

    object_id = models.PositiveIntegerField(
        verbose_name=_('parser id'),
        help_text=_('The id of the object that will parse the data.')
    )
    field_parser = GenericForeignKey()

    target_field = models.ForeignKey(
        BottleField,
        help_text=_('The name of the field in the condenser\'s bottle, '
                    'where the parsed data will be stored.')
    )

    def __init__(self, *args, **kwargs):
        super(Fitting, self).__init__(*args, **kwargs)

        if self.CONTENT_TYPES is None:
            raise NotImplementedError('CONTENT_TYPES need to be defined '
                                      'for this model.')

    def __str__(self):
        if self.pk:
            return "%s <- %s (%s)" % (self.target_field, self.field_parser,
                                      self.fitting_type)
        else:
            return super(Fitting, self).__str__()

    class Meta(object):
        """Metadata options."""

        abstract = True

    def clean(self):
        super(Fitting, self).clean()

        if hasattr(self, 'condenser') and hasattr(self, 'target_field'):
            if hasattr(self.condenser, 'bottle') \
                    and not self._field_is_in_bottle():
                raise ValidationError(
                    _('The selected target field is not compatible with '
                      'the condenser\'s bottle.'))

            elif self._target_is_embedded_doc() and not self.is_condenser():
                raise ValidationError(
                    _('If the target field is an EmbeddedDocument, '
                      'the content type must be a condenser.'))

            elif not self._target_is_embedded_doc() and self.is_condenser():
                raise ValidationError(
                    _('Unless the target field is an EmbeddedDocument, '
                      'the content type must be a parser.'))

    @property
    def _content_class(self):
        """
        Returns the class for the type of fitting, which can be either a Parser
        or another Condenser.
        """
        return self.content_type.model_class()

    @property
    def fitting_type(self):
        """
        Returns the name of the class for the type of fitting, which can be
        either a Parser or another Condenser.
        """
        return self.content_type.model

    @property
    def target_field_name(self):
        """
        Returns the name of the field used to store the value extracted from the
        raw data.
        """
        return self.target_field.field_name

    @property
    def target_field_type(self):
        """
        Returns a string indicating the type of field used to store the value
        extracted from the raw data (e.g., "CharField").
        """
        return self.target_field.field_type

    def _target_is_embedded_doc(self):
        """
        Returns a Boolean indicating whether the target_field is an
        EmbeddedDocument.
        """
        return self.target_field_type == 'EmbeddedDocument'

    def _get_condenser_fields(self):
        """
        Returns a QuerySet of BottleFields associated with the Fitting's
        Condenser.
        """
        return self.condenser.get_fields()

    def _field_is_in_bottle(self):
        """
        Returns a Boolean indicating whether the target_field is present in the
        Bottle associated with the chosen Condenser.
        """
        return self.condenser.field_is_in_bottle(self.target_field)

    def is_parser(self):
        """
        Returns a Boolean indicating whether the Fitting is a Parser.
        """
        return issubclass(self._content_class, Parser)

    def is_condenser(self):
        """
        Returns a Boolean indicating whether the Fitting is a Condenser.
        """
        return issubclass(self._content_class, Condenser)

    def process(self, data, *args, **kwargs):
        """
        Takes a dictionary of data and returns the condensed result.
        """
        # NOTE: for this to work, both Condensers and Parsers need a process()
        # method to handle data, since the field_parser can be either a
        # Condenser or a Parser
        return self.field_parser.process(data, *args, **kwargs)
