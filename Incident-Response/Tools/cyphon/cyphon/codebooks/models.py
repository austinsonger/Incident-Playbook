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
Defines CodeName, RealName, and CodeBook models for redacting text fields.
"""

# standard library
from collections import OrderedDict
import json
import logging
import re

# third party
from django.conf import settings
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

# local
from companies.models import Company
from utils.validators.validators import regex_validator

_CODEBOOK_SETTINGS = settings.CODEBOOKS

_LOGGER = logging.getLogger(__name__)


class CodeNameManager(models.Manager):
    """
    Adds methods to the default model manager.
    """

    def get_by_natural_key(self, code):
        """
        Allow retrieval of a RealName by its natural key instead of its
        primary key.
        """
        try:
            return self.get(code=code)
        except ObjectDoesNotExist:
            _LOGGER.error('%s "%s" does not exist', self.model.__name__, code)

    def get_queryset(self):
        """
        Overrides the default get_queryset method to select related
        RealNames.
        """
        default_queryset = super(CodeNameManager, self).get_queryset()
        return default_queryset.prefetch_related('realnames')


class CodeName(models.Model):
    """
    Defines a name and a code name that can be used in its place.

    Attributes:
        code: a string to be used in place of associated RealNames
    """
    code = models.CharField(max_length=255, unique=True)

    objects = CodeNameManager()

    class Meta:
        """
        Metadata options for a Django Model.
        """
        ordering = ['code']

    def __str__(self):
        return self.code

    @property
    def formatted_codename(self):
        """
        Returns a formatted version of the codename.
        """
        prefix = _CODEBOOK_SETTINGS['CODENAME_PREFIX']
        suffix = _CODEBOOK_SETTINGS['CODENAME_SUFFIX']
        return prefix + self.code + suffix


class RealNameManager(models.Manager):
    """
    Adds methods to the default model manager.
    """

    def get_by_natural_key(self, regex):
        """
        Allow retrieval of a RealName by its natural key instead of its
        primary key.
        """
        try:
            return self.get(regex=regex)
        except ObjectDoesNotExist:
            _LOGGER.error('%s "%s" does not exist', self.model.__name__, regex)


class RealName(models.Model):
    """
    Defines a string that should be replaced with a code name.

    Attributes:
        regex: a string representing a regular expression that should be replaced
            with a CodeName
        code: a ForeignKey to the CodeName which should be used in place of the
            RealName
        rank: an integer representing the order in which the RealName should
            be replaced, relative to other RealNames. RealNames that are
            substrings of other RealNames should be assigned a higher number
            (lower rank).
    """
    regex = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_('regex'),
        validators=[regex_validator],
        help_text=_('The regular expression used to identify substrings that '
                    'should be replaced with the code name.')
    )
    codename = models.ForeignKey(
        CodeName,
        related_name='realnames',
        related_query_name='realname',
        verbose_name=_('CodeName'),
        help_text=_('The string that will replace the real name.')
    )
    rank = models.IntegerField(
        default=0,
        help_text=_('The order in which the regex should be '
                    'searched for and replaced.'))

    # NOTE: Real names that are substrings of other names should be assigned a
    # larger number so they are searched for only after those longer names have
    # been replaced. Conversely, longer real names should be assigned smaller
    # numbers.

    objects = RealNameManager()

    class Meta:
        """
        Metadata options for a Django Model.
        """
        ordering = ['rank', 'regex']

    def __str__(self):
        return '%s: %s' % (self.codename, self.regex)

    @property
    def _formatted_codename(self):
        """
        Returns a formatted version of the Realname's CodeName string.
        """
        return self.codename.formatted_codename

    def to_dict(self):
        """
        Returns a dictionary in which the key is the RealName.name and the value
        is the RealName.code.
        """
        return {self.regex: str(self.codename)}

    def redact(self, text):
        """
        Takes a text string and returns a redacted version of the text
        using the RealNames's formatted CodeName.
        """
        pattern = re.compile(self.regex, re.IGNORECASE)
        return pattern.sub(self._formatted_codename, text)


class CodeBookManager(models.Manager):
    """
    Adds methods to the default model manager.
    """

    def get_queryset(self):
        """
        Overrides the default get_queryset method to prefetch related
        CodeNames.
        """
        default_queryset = super(CodeBookManager, self).get_queryset()
        return default_queryset.prefetch_related('codenames__realnames')

    def get_by_natural_key(self, company_name):
        """
        Allow retrieval of a Codebook by its natural key instead of its
        primary key.
        """
        try:
            company = Company.objects.get_by_natural_key(company_name)
            return self.get(company=company)
        except ObjectDoesNotExist:
            _LOGGER.error('Codebook for Company "%s" does not exist',
                          company_name)


class CodeBook(models.Model):
    """
    Defines a collection of CodeNames that can be used to redact teaser data.
    """
    company = models.OneToOneField(Company, primary_key=True)
    codenames = models.ManyToManyField(CodeName)

    objects = CodeBookManager()

    class Meta:
        """
        Metadata options for a Django Model.
        """
        ordering = ['company']

    def __str__(self):
        return str(self.company)

    @cached_property
    def realnames(self):
        """
        Returns a QuerySet of RealNames associated with the CodeBook,
        sorted by rank.
        """
        realnames = []
        for codename in self.codenames.all():
            realnames.extend(codename.realnames.all())
        realnames.sort(key=lambda x: x.rank)
        return realnames

    def _get_codename_dict(self):
        """
        Returns a dictionary in which the keys are RealNames and the values
        are their corresponding CodeNames.
        """
        codes = OrderedDict()
        for realname in self.realnames:
            codes.update(realname.to_dict())
        return codes

    def preview(self):
        """
        Returns a string representation of a dictionary of the RealNames
        and CodeNames associated with the CodeBook.
        """
        codes = self._get_codename_dict()
        return json.dumps(codes, indent=4)

    def redact(self, text):
        """
        Takes a text string and returns a redacted version of the text
        using the CodeBook's CodeNames.
        """
        for realname in self.realnames:
            text = realname.redact(text)
        return text
