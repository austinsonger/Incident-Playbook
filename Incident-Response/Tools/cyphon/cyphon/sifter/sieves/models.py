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
Defines Rule, Sieve, and SieveNode classes.

======================  =======================================================
Class                   Description
======================  =======================================================
:class:`~Rule`          An abstract base class for models that define rules.
:class:`~StringRule`    A Rule subclass for use with a string.
:class:`~FieldRule`     A Rule subclass for use with a dictionary.
:class:`~Sieve`         An abstract base class for models that define rulesets.
:class:`~SieveManager`  Model Manager for Sieves.
======================  =======================================================

"""

# standard library
import logging
import operator
import re
import sre_constants

# third party
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

# local
from cyphon.models import GetByNameManager
from cyphon.choices import LOGIC_CHOICES, RANGE_CHOICES, REGEX_CHOICES
from lab.procedures.models import Protocol
from utils.parserutils.parserutils import get_dict_value
from utils.validators.validators import regex_validator

LOGGER = logging.getLogger(__name__)


class Rule(models.Model):
    """An abstract base class for models that define rules.

    Attributes
    ----------
    name : str
        The name of the Rule.

    protocol : Protocol
        An optional |Protocol| that classifies the input data so the
        result can be examined by the Rule. If no |Protocol| is specified,
        the raw data is examined instead.

    value : str
        A |str| to be substituted for 'x' in the operator attribute.

    is_regex : bool
        Whether the value should be interpreted as a regular expression.

    case_sensitive : bool
        Whether a regex value should ignore case.

    negate : bool
        Whether the Rule should be evaluated as True when data does NOT
        match the regex condition.

    """

    name = models.CharField(
        max_length=40,
        unique=True,
        help_text=_('It\'s a good idea to name rules after the data '
                    'they examine and the comparison they make, e.g. '
                    '"log_contains_WARNING."')
    )
    protocol = models.ForeignKey(
        Protocol,
        blank=True,
        null=True,
        default=None,
        help_text=_('An optional Protocol to apply to the data so the '
                    'result can be examined by the Rule. If no Protocol '
                    'is specified, the raw data is examined instead.')
    )
    value = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text=_('The value to compare the data against. If using regex, the output of the regex is used for comparison.')
    )
    is_regex = models.BooleanField(
        default=False,
        verbose_name=_('regular expression'),
        help_text=_('Whether the value should be interpreted '
                    'as a regular expression.')
    )
    case_sensitive = models.BooleanField(
        default=False,
        help_text=_('Whether the comparison should be case sensitive.')
    )
    negate = models.BooleanField(
        default=False,
        help_text=_('Whether the Rule should be evaluated as True '
                    'if the data does NOT match the condition.')
    )

    class Meta(object):
        """Metadata options."""

        abstract = True
        ordering = ['name']

    def __str__(self):
        return self.name

    def clean(self):
        """
        Validates the model as a whole.

        See also
        --------
        Refer to Django's documentation on `cleaning and validating`_
        fields that depend on each other.

        """
        super(Rule, self).clean()
        if self.operator != 'EmptyField' and self.value in ['', None]:
            raise ValidationError(_('The value field is required.'))

        if self.operator.startswith('FloatField'):
            try:
                float(self.value)
            except ValueError:
                raise ValidationError(_('A numeric value is required '
                                        'for this type of comparison.'))
        if self.is_regex:
            regex_validator(self.value)

    def _preprocess(self, data):
        self.protocol.process(data)

    def _get_comparison_value(self, data):
        """
        Takes a dictionary or a string of data. If a protocol is included in the
        Rule, processes the data with the protocol and returns the result.
        Otherwise, returns the original data value.
        """
        if self.protocol is not None:
            return self._preprocess(data)

        return data

    def _create_regex(self):
        """
        Returna a regular expression pattern for Rule.value based on Rule.operator,
        with special characters escaped for non-regex values.
        """
        if not self.is_regex:
            value = re.escape(self.value)
        else:
            value = self.value
        operator_value = self._get_operator_value()
        return operator_value.replace('x', value)

    def _get_string(self, data):
        """
        Takes a data object and returns it in the form of a string. This
        method should be overridden in derived classes.
        """
        raise NotImplementedError()

    def _get_operator_type(self):
        """
        Returns the type of field that is being examined by the rule.
        """
        return self.operator.split(':')[0]

    def _get_operator_value(self):
        """
        Returns the type of field that is being examined by the rule.
        """
        return self.operator.split(':')[1]

    def _matches_regex(self, data):
        """
        Takes a dictionary or a string of data and returns True if the data
        matches the Rule's regex. Otherwise, returns False.
        """
        regex = self._create_regex()
        string = self._get_string(data)
        args = [regex, string]

        if not self.case_sensitive:
            args.append(re.IGNORECASE)

        try:
            if re.search(*args):
                return True
        except sre_constants.error:
            LOGGER.error('Cannot parse the regex "%s" for %s %s',
                         regex, self.__class__.__name__, self.id)

        return False

    def _check_value(self, value):
        """
        Takes a value and checks it against the Rule's logic. Returns
        the result as a Boolean.
        """
        return self._matches_regex(value)

    def is_match(self, data):
        """
        Takes a dictionary or a string of data and returns True if the data meets
        the Rule's criterion. Otherwise, returns False.
        """
        value = self._get_comparison_value(data)
        match = self._check_value(value)

        if self.negate:
            return not match

        return match


class StringRule(Rule):
    """A Rule subclass for use with a string.

    Attributes
    ----------
    name : str
        The name of the Rule.

    protocol : Protocol
        An optional |Protocol| that classifies the input data so the
        result can be examined by the Rule. If no |Protocol| is specified,
        the raw data is examined instead.

    value : str
        A |str| to be substituted for 'x' in the operator attribute.

    is_regex : bool
        Whether the value should be interpreted as a regular expression.

    case_sensitive : bool
        Whether a regex value should ignore case.

    negate : bool
        Whether the Rule should be evaluated as True when data does NOT
        match the regex condition.

    operator : str
        The type of comparison to make.

    """

    operator = models.CharField(
        max_length=40,
        choices=REGEX_CHOICES,
        help_text=_('The type of comparison to make.')
    )

    class Meta(object):
        """Metadata options."""

        abstract = True
        ordering = ['name']

    def _get_string(self, data):
        """
        Takes a data object and returns it in the form of a string.
        """
        return str(data)


class FieldRule(Rule):
    """A Rule subclass for use with a dictionary.

    Attributes
    ----------
    name : str
        The name of the Rule.

    protocol : Protocol
        An optional |Protocol| that classifies the input data so the
        result can be examined by the Rule. If no |Protocol| is specified,
        the raw data is examined instead.

    value : str
        A |str| to be substituted for 'x' in the operator attribute.

    is_regex : bool
        Whether the value should be interpreted as a regular expression.

    case_sensitive : bool
        Whether a regex value should ignore case.

    negate : bool
        Whether the Rule should be evaluated as True when data does NOT
        match the regex condition.

    operator : str
        The type of comparison to make.

    field_name : str
        The name of the data field that should be examined by the Rule.

    """

    DATAFIELD_CHOICES = (
        ('EmptyField', 'is null'),
    )

    operator = models.CharField(
        max_length=40,
        choices=list(REGEX_CHOICES) + list(RANGE_CHOICES) + list(DATAFIELD_CHOICES),
        help_text=_('The type of comparison to make.')
    )
    field_name = models.CharField(
        max_length=40,
        help_text=_('The name of the data field that should be examined '
                    'by the Rule.')
    )

    class Meta(object):
        """Metadata options."""

        abstract = True
        ordering = ['name']

    def _get_value(self, data):
        """
        Takes a dictionary and returns the value for the key specified by the
        field_name.
        """
        return get_dict_value(self.field_name, data)

    def _get_string(self, data):
        """
        Takes a dictionary and returns the value for the key specified by the
        field_name.
        """
        value = self._get_value(data)
        return str(value)

    def _is_null(self, data):
        """

        """
        value = self._get_value(data)
        return value is None

    def _numeric_match(self, data):
        """

        """
        operators = {
            '>': operator.gt,
            '>=': operator.ge,
            '<': operator.lt,
            '<=': operator.le
        }
        try:
            comparison = self._get_operator_value()
            value = self._get_value(data)
            return operators[comparison](float(value), float(self.value))
        except (ValueError, TypeError):  # catch TypeError if value is None
            return False

    def _check_value(self, value):
        """
        Takes a value and checks it against the Rule's logic. Returns the result
        as a Boolean.
        """
        operator_type = self._get_operator_type()
        methods = {
            'CharField': self._matches_regex,
            'EmptyField': self._is_null,
            'FloatField': self._numeric_match,
        }

        func = methods[operator_type]
        return func(value)


class SieveManager(GetByNameManager):
    """
    Adds methods to the default model manager.
    """

    def get_sieves_with_chutes(self):
        """
        Returns a QuerySet of all Sieves associated with Chutes.
        """
        default_queryset = self.get_queryset()
        return default_queryset.filter(chute__isnull=False)

    def _get_node_model(self):
        """
        Returns the SieveNode subclass associated with the Sieve.
        """
        return self.model._meta.get_field('node').related_model

    def create_default_sieve(self):
        """

        """
        node_model = self._get_node_model()
        sieves = self.get_sieves_with_chutes()

        default_sieve = self.model(name='default')
        default_sieve.save()
        default_sieve.nodes.all().delete()
        for sieve in sieves:
            content_type = ContentType.objects.get_for_model(node_model)
            default_sieve.nodes.create(content_type=content_type,
                                       object_id=sieve.pk)
        return default_sieve


class Sieve(models.Model):
    """An abstract base class for models that define rulesets.

    A Sieve is associated with one or more SieveNodes.

    Attributes
    ----------
    name : str
        The name of the Sieve.

    logic : str
        The logic used to combine rulesets, which can be 'AND' or 'OR'.
        Default is 'AND'.

    negate : bool
        Whether the Sieve should be evaluated as True when data does NOT
        match the regex condition.

    """

    name = models.CharField(max_length=40, unique=True)
    logic = models.CharField(
        max_length=3,
        choices=LOGIC_CHOICES,
        default='AND',
        help_text=_('Choose "AND" if all nodes should return True. '
                    'Choose "OR" if one or more nodes should return True.'))
    negate = models.BooleanField(default=False)

    class Meta(object):
        """Metadata options."""

        abstract = True
        ordering = ['name']

    def __str__(self):
        return self.name

    def _matches_all(self, data):
        """
        Takes a dictionary of data and returns True if the data matches all
        Rules in the RuleSet. Otherwise, returns False.
        """
        for node in self.nodes.all():
            if not node.is_match(data):
                return False
        return True

    def _matches_any(self, data):
        """
        Takes a dictionary of data and returns True if the data matches
        any Rule in the RuleSet. Otherwise, returns False.
        """
        for node in self.nodes.all():
            if node.is_match(data):
                return True
        return False

    def get_node_number(self):
        """
        Returns the number of nodes associated with the Sieve.
        """
        return self.nodes.count()

    get_node_number.short_description = _('nodes')

    def is_match(self, data):
        """
        Takes a dictionary of data and returns True if the data meet the
        criteria of the RuleSet. Otherwise, returns False.
        """
        if self.logic == 'AND':
            match = self._matches_all(data)
        elif self.logic == 'OR':
            match = self._matches_any(data)

        if self.negate:
            return not match
        else:
            return match


class SieveNode(models.Model):
    """A reference to a Rule or a Sieve.

    Allows construction of nested Sieves for complex rules.

    The content_type choices should be limited to a derived class of Rules and
    a derived class of Sieves specifically designed to handle that class of
    Rules. This ensures that all Rules within a RuleSet handle the same type of
    data (strings, dictionaries, etc.).

    For example:

        class MyRule(sifter.sieves.FieldRule):
            pass

        class MyRuleSet(sifter.sieves.RuleSet):
            pass

        class MyRuleNode(sifter.sieves.RuleSetNode):
            RULE = models.Q(app_label='myrules', model='myrule')
            RULESET = models.Q(app_label='myrules', model='myruleset')
            CONTENT_TYPES = RULE | RULESET

            content_type = models.ForeignKey(ContentType, limit_choices_to=CONTENT_TYPES)
            object_id = models.PositiveIntegerField()
            node_object = GenericForeignKey()

    """

    object_id = models.PositiveIntegerField()
    node_object = GenericForeignKey()

    class Meta(object):
        """Metadata options."""

        abstract = True
        ordering = ['sieve']
        unique_together = ('sieve', 'content_type', 'object_id')

    def __str__(self):
        return "%s (%s)" % (self.node_object, self.node_type)

    def _node_obj_is_valid(self, sieve=None):
        """
        Determines whether the SieveNode contains a recursion.
        """
        sieve = sieve or self.sieve
        if isinstance(self.node_object, Sieve):
            if sieve == self.node_object:
                return False
            else:
                for node in self.node_object.nodes.all():
                    if not node._node_obj_is_valid(sieve):
                        return False
        return True

    def clean(self):
        """
        Validates the model as a whole.
        """
        super(SieveNode, self).clean()

        if not self._node_obj_is_valid():
            raise ValidationError(_('To prevent recursion, a SieveNode cannot '
                                    'point to a Sieve that is its parent '
                                    'Sieve or contains its parent Sieve.'))

    @property
    def node_type(self):
        """
        Returns the name of the class for the type of node, which can be
        either a DataRule or a DataSieve.
        """
        return self.content_type.model

    def is_match(self, data):
        """
        Takes a data object and returns True if the data meets the Clause's
        criterion. Otherwise, returns False.
        """
        return self.node_object.is_match(data)
