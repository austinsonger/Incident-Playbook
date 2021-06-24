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
Defines forms for MailFittings and MailCondensers.
"""

# local
from cyphon.autocomplete import AutoCompleteModelFormMixin, ChoiceWidget
from sifter.condensers.forms import (
    CondenserForm,
    FittingForm,
    FittingInlineForm,
    ParserForm
)
from .models import MailCondenser, MailFitting, MailParser


class MailParserForm(ParserForm):
    """
    Defines a form for adding or updating a MailCondenser using autocomplete
    fields.
    """

    class Meta(ParserForm.Meta):
        model = MailParser


class MailCondenserForm(CondenserForm):
    """
    Defines a form for adding or updating a MailCondenser using autocomplete
    fields.
    """

    class Meta(CondenserForm.Meta):
        model = MailCondenser


class MailFittingForm(FittingForm, AutoCompleteModelFormMixin):
    """
    Defines a form for adding or updating a MailFitting using autocomplete
    fields.
    """

    class Meta(FittingForm.Meta):
        model = MailFitting
        autocomplete_names = {
            'target_field': 'FilterTargetFieldsByMailCondenser'
        }
        widgets = {
            'target_field': ChoiceWidget('FilterTargetFieldsByMailCondenser'),
        }


class MailFittingInlineForm(FittingInlineForm):
    """
    Defines an inline form for adding or updating a MailFitting using
    autocomplete fields.
    """

    class Meta(FittingInlineForm.Meta):
        model = MailFitting
        widgets = {
            'target_field': ChoiceWidget('FilterTargetFieldsByBottle'),
        }
