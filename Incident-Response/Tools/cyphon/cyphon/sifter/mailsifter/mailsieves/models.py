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
Defines Rule and RuleSet classes.
"""

# third party
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

# local
from cyphon.choices import EMAIL_FIELD_CHOICES, REGEX_CHOICES
from cyphon.models import GetByNameManager
from sifter.mailsifter import accessors
from sifter.sieves.models import Rule, Sieve, SieveManager, SieveNode


class MailRule(Rule):
    """
    A Rule subclass for examining email messages.
    """
    operator = models.CharField(
        max_length=40,
        choices=REGEX_CHOICES,
        help_text=_('The type of comparison to make.')
    )
    field_name = models.CharField(max_length=40,
                                  choices=EMAIL_FIELD_CHOICES)

    objects = GetByNameManager()

    def _get_string(self, data):
        """
        Takes an email Message object and returns the Message component
        indicated by the MailRule's field_name.
        """
        value = accessors.get_email_value(self.field_name, data)
        return str(value)


class MailSieve(Sieve):
    """
    A RuleSet subclass for examining email messages.
    """
    objects = SieveManager()


class MailSieveNode(SieveNode):
    """
    A RuleSetNode subclass for examining email messages.
    """
    _RULE = models.Q(app_label='mailsieves', model='mailrule')
    _RULESET = models.Q(app_label='mailsieves', model='mailsieve')
    _CONTENT_TYPES = _RULE | _RULESET

    sieve = models.ForeignKey(
        MailSieve,
        related_name='nodes',
        related_query_name='node',
        help_text=_('A rule or rule set to assign to the node.')
    )
    content_type = models.ForeignKey(ContentType,
                                     limit_choices_to=_CONTENT_TYPES,
                                     verbose_name=_('node type'))
