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
Defines a Teaser base class used to display a teaser for a document.
A Teaser provides basic information about the data, specifing "Who,"
"What," "When," and "Where."
"""

# standard library
import datetime
import json

# third party
from django.conf import settings
from django.core import serializers
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

# local
from cyphon.choices import GEOCOORDINATE_CHOICES
from utils.geometry.shapes import convert_to_point
from utils.parserutils.parserutils import get_dict_value
from utils.dateutils.dateutils import date_from_str

_DISTILLERY_SETTINGS = settings.DISTILLERIES
_TEASER_SETTINGS = settings.TEASERS


class Teaser(models.Model):
    """
    A Teaser maps the fields of a document to a standard set of fields
    used to construct a preview of the document. This preview answers
    basic questions about the nature of the data, such as Who?, What?,
    When?, and Where?. Teasers can be used to display documents with
    different schemas in a common format.

    Attributes
    ----------
    author : str
        The name of a CharField representing the person associated with
        the document. (Answers the question, "When?")

    title : str, optional
        The name of a CharField summarizing the document. (Answers the
        question, "What?")

    content : str
        The name of a CharField containing the main content of the
        document. (Answers the question, "What?")

    location : str
        The name of a LocationField representing the location associated
        with the document. (Answers the question, "Where?")

    location_format : str
        A |str| defining the order of geocoordinates. Choices are
        limited to |GEOCOORDINATE_CHOICES|.

    datetime : str
        The name of a DateTimeField representing the date when the
        document was generated or saved. (Answers the question, "When?")
        This should refer to a field whose value is a |datetime| object.

    date_string : str
        The name of a CharField representing the date when the
        document was generated or saved. This is an alternative to
        :attr:`~Teaser.datetime`, which refers to a DateTimeField
        (whose value is a |datetime| object).

    date_format : str
        A |str| containing |datetime| `format codes`_ for parsing
        the value of the :attr:`~Teaser.date_string` field.

    Notes
    -----
    Nested fields (i.e., fields in embedded documents) should be
    indicated with dot notation (e.g. 'user.name').

    Notes
    -----
    The date for a teaser will be taken from the :attr:`~Teaser.datetime`
    field, if a value is provided. If not, the :attr:`~Teaser.date_string`
    field will be used as a fallback.

    Warning
    -------
    A teaser contains a `collection` field representing the |Collection|
    in which the data is stored. This field is NOT redacted. Be
    careful in using it if there is sensitive information in the
    |Collection| or |Warehouse| name in which the data is stored.

    _format codes: https://docs.python.org/3.4/library/datetime.html#strftime-and-strptime-behavior

    """
    author = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255)
    content = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    location_format = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        choices=GEOCOORDINATE_CHOICES,
        default='LNG/LAT'
    )
    datetime = models.CharField(max_length=255, blank=True, null=True)
    date_string = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text=_('An alternative to a datetime field. Use if the date is '
                    'a string rather than a DateTime object.')
    )
    date_format = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text=_('If a date string is used, please enter its date format, '
                    'if known (e.g., %Y-%m-%d %H:%M:%S %z).')
    )

    REDACTED_FIELDS = ('author', 'title', 'content')
    """`tuple`

        Fields whose content should be redacted if the current |AppUser|
        has :attr:`~appusers.models.AppUser.use_redaction` set to |True|.
        Redaction is performed using |CodeBooks|.

    """

    TEXT_FIELDS = ('author', 'title', 'content')
    """`tuple`

        Fields whose values should be included in full-text searches of
        teasers.

    """

    class Meta:
        abstract = True

    def clean(self):
        """
        Overrides the default clean() method.
        """
        super(Teaser, self).clean()
        if self.datetime and self.date_string:
            raise ValidationError(
                _('Please choose either a datetime field or a date '
                  'string field, but not both.'))

        # if self.date_string and not self.date_format:
        #     raise ValidationError(
        #         _('Please define a date format for the date string field '
        #           '(e.g., %Y-%m-%d %H:%M:%S %z).'))

    def _to_dict(self):
        """
        Returns a dictionary in which the keys are the fields of the
        Teaser model and the values are the object instance's values for
        those fields. Location and date-related fields are not included.
        """
        json_data = serializers.serialize('json', [self])
        data = json.loads(json_data)
        fields_dict = data[0]['fields']
        return fields_dict

    @staticmethod
    def _get_collection_name(data):
        """
        Takes a dictionary of distilled data and returns a string
        representing the Collection where the data is stored.
        """
        if data is not None:
            raw_data = get_dict_value(_DISTILLERY_SETTINGS['RAW_DATA_KEY'],
                                      data)
            if raw_data:
                try:
                    return '.'.join([
                        raw_data.get(_DISTILLERY_SETTINGS['BACKEND_KEY']),
                        raw_data.get(_DISTILLERY_SETTINGS['WAREHOUSE_KEY']),
                        raw_data.get(_DISTILLERY_SETTINGS['COLLECTION_KEY'])
                    ])
                except TypeError:
                    return None
            else:
                return None

    @staticmethod
    def _trim_field_value(value):
        """
        Takes a field value and trims it to TEASER_CHAR_LIMIT if
        necessary.
        """
        limit = _TEASER_SETTINGS['CHAR_LIMIT']
        if isinstance(value, str) and len(value) > limit:
            return value[:limit]
        else:
            return value

    def _get_date_value(self, data):
        """
        Takes a dictionary of data and attempts to return the date field.
        If none exists, returns None.
        """
        if self.datetime:
            return get_dict_value(self.datetime, data)
        elif self.date_string:
            return get_dict_value(self.date_string, data)

    def get_location(self, data):
        """Return the value of the location field.

        Parameters
        ----------
        data : |dict|
            A document from which to extract the date field.

        Returns
        -------
        |Point| or |None|
            The value of the location field.

        """
        location = get_dict_value(self.location, data)
        if location:
            return convert_to_point(location, self.location_format)

    def _get_teaser_data(self, data):
        """
        Takes a dictionary of distilled data and returns a dictionary of
        data that can be used to show a teaser (taste) of that data.
        """
        sample = {}
        field_dict = self._to_dict()

        for key in self.TEXT_FIELDS:
            field_name = field_dict[key]
            if field_name:
                sample[key] = get_dict_value(field_name, data)
            else:
                sample[key] = None

        sample['date'] = self.get_date(data)
        sample['location'] = self.get_location(data)
        sample['collection'] = self._get_collection_name(data)

        return sample

    def get_date_field(self):
        """Get the name of the date field.

        Returns
        -------
        str
            The name of the field used for the |Teaser|'s date.

        """
        if self.datetime:
            return self.datetime
        elif self.date_string and self.date_format:
            return self.date_string

    def get_date(self, data):
        """Return the value of the date field.

        Parameters
        ----------
        data : |dict|
            A document from which to extract the date field.

        Returns
        -------
        |datetime| or |None|
            The value of the date field.

        """
        date = self._get_date_value(data)
        if isinstance(date, datetime.datetime):
            return date
        elif date:
            return date_from_str(str(date), self.date_format)

    def get_sample(self, data):
        """Return a teaser for the data.

        Parameters
        ----------
        data : |dict|
            Data from which to create a teaser.

        Returns
        -------
        |dict|
            A teaser of the data.

        """
        teaser_data = self._get_teaser_data(data)
        sample = {}

        for (key, val) in teaser_data.items():
            if key in self.TEXT_FIELDS:
                sample[key] = self._trim_field_value(val)
            else:
                sample[key] = val

        return sample

    def get_blind_sample(self, data, codebook):
        """Return a redacted teaser for the data.

        Parameters
        ----------
        data : |dict|
            Data from which to create a redacted teaser.

        codebook : |CodeBook|
            A |CodeBook| for redacting the teaser.

        Returns
        -------
        |dict|
            A redacted teaser of the data.

        """
        teaser_data = self._get_teaser_data(data)
        sample = {}

        for (key, val) in teaser_data.items():

            # redact fields before trimming them to avoid the risk of
            # of regular expressions not catching truncated words
            if isinstance(val, str) and key in self.REDACTED_FIELDS:
                field_value = codebook.redact(val)
            else:
                field_value = val

            # trim fields after redaction
            if key in self.TEXT_FIELDS:
                sample[key] = self._trim_field_value(field_value)
            else:
                sample[key] = field_value

        return sample

    def get_text_fields(self):
        """Return a list of names of searchable text fields.

        Returns
        -------
        |list| of |str|
            Names of searchable text fields associated with the Teaser.

        """
        taste_dict = self._to_dict()
        fields = []

        for field in self.TEXT_FIELDS:
            field_name = taste_dict[field]
            fields.append(field_name)

        fields.sort()
        return fields
