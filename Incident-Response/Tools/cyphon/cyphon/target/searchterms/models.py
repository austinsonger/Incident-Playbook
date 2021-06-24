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
Defines a class for a search term, which can be a keyword or phrase.
"""

# standard library
import logging

# standard library
from copy import deepcopy
from django.core.exceptions import ObjectDoesNotExist
import re

# third party
from django.db import models

_LOGGER = logging.getLogger(__name__)


class SearchTermManager(models.Manager):
    """Manage |SearchTerm| objects.

    Adds methods to the default Django model manager.
    """

    def get_by_natural_key(self, term):
        """Get a |SearchTerm| by its natural key.

        Allows retrieval of a |SearchTerm| by its natural key instead of
        its primary key.

        Parameters
        ----------
        term : str
            The SearchTerm's `~SearchTerm.term`.

        Returns
        -------
        |SearchTerm|
            The |SearchTerm| associated with the natural key.

        """
        try:
            return self.get(term=term)
        except ObjectDoesNotExist:
            _LOGGER.error('%s "%s" does not exist', self.model.__name__, term)


class SearchTerm(models.Model):
    """
    A keyword or phrase to be used in a social media query.
    """
    term = models.CharField(max_length=255, unique=True)
    negate = models.BooleanField(default=False)

    objects = SearchTermManager()

    def __str__(self):
        if self.negate:
            prefix = 'NOT '
        else:
            prefix = ''
        return '%s"%s"' % (prefix, self.term)

    @property
    def tag(self):
        """
        Removes any spaces from a term and returns the result as a single string.
        """
        return self.term.replace(' ', '')

    def parse_term(self):
        """
        Returns a list of words contained in the term.
        """
        return re.split(' ', self.term)

    def is_phrase(self):
        """
        Returns True if the search term is a phrase.
        """
        words = self.parse_term()

        if len(words) > 1:
            return True
        else:
            return False

    def create_term_from_tag(self):
        """
        Transforms a phrase into a tag and returns a new SearchTerm object
        containing the tag.
        """
        new_term = deepcopy(self)
        new_term.term = self.tag
        return new_term

    def create_terms_from_words(self):
        """
        Splits a phrase into its component words and returns a list of new
        SearchTerm objects for each word.
        """
        new_terms = []
        words = self.parse_term()

        for word in words:
            new_term = deepcopy(self)
            new_term.term = word
            new_terms.append(new_term)

        return new_terms

    def create_terms_from_phrase(self):
        """
        If the SearchTerm is a phrase, returns a list containing SearchTerms for
        each individual word of the phrase, as well as a SearchTerm with the
        phrase as a tag (i.e., without spaces between words). Otherwise, returns
        a list containing only the original SearchTerm.
        """
        # if the phrase is supposed to be negated, return an empty list,
        # because we don't want a query that will negate the words individually
        if self.negate:
            return []

        elif self.is_phrase():

            new_terms = []

            words = self.create_terms_from_words()
            new_terms.extend(words)

            tag = self.create_term_from_tag()
            new_terms.append(tag)

            return new_terms

        else:
            return [self]

    def wrap_in_quotes(self):
        """
        Returns the SearchTerm wrapped in double quotation marks.
        """
        self.term = '\"%s\"' % (self.term)
        return self
