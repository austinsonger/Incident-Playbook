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
from email import message_from_string

# third party
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

# local
from cyphon.models import GetByNameManager
from cyphon.choices import EMAIL_FIELD_CHOICES
from parsers.models import StringParser
from sifter.condensers.models import Condenser, Fitting
from sifter.mailsifter.attachments import save_attachment
from sifter.mailsifter.accessors import get_email_value


class MailParser(StringParser):
    """
    Parses an email Message object.

    name : str

    method : str

    regex : str

    formatter : str

    source_field : str

    """
    source_field = models.CharField(
        max_length=255,
        choices=EMAIL_FIELD_CHOICES,
        help_text=_('The email field from which data will be extracted.')
    )

    def clean(self):
        super(MailParser, self).clean()
        choices = [item[0] for item in EMAIL_FIELD_CHOICES]
        if self.source_field not in choices:
            raise ValidationError(
                _('The selected source field is not a valid email field.'))
        if self._has_attachment() and self.method != 'COPY':
            raise ValidationError(
                _("If the source field refers to an attachment, "
                  "the method must be 'COPY'."))

    def _has_attachment(self):
        """

        """
        return 'attachment' in self.source_field.lower()

    @staticmethod
    def _save_attachments(value, company):
        """

        """
        if isinstance(value, list):
            return [save_attachment(attachment, company) for attachment in value]
        else:
            return save_attachment(value, company)

    def run_test(self, string):
        """

        """
        email = message_from_string(string)
        if not email:
            return 'Sorry! The string you entered could not be converted to '\
                   'an email. Please enter the raw source of an email to test.'
        return self.process(email)

    def process(self, email, company=None):
        """
        Takes a value and returns a parsed result.
        """
        value = get_email_value(self.source_field, email)

        if self._has_attachment() and value:
            value = self._save_attachments(value, company)

        result = self._parse(value)

        if self.formatter:
            return self._apply_template(result)
        else:
            return result


class MailCondenser(Condenser):
    """

    """
    objects = GetByNameManager()


class MailFitting(Fitting):
    """

    """
    CONDENSER = models.Q(app_label='mailcondensers', model='mailcondenser')
    PARSER = models.Q(app_label='mailcondensers', model='mailparser')
    CONTENT_TYPES = PARSER | CONDENSER

    condenser = models.ForeignKey(MailCondenser, related_name='fittings',
                                  related_query_name='fitting')
    content_type = models.ForeignKey(ContentType,
                                     limit_choices_to=CONTENT_TYPES,
                                     verbose_name=_('parser type'))
