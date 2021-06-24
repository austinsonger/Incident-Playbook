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
Defines forms for DataFittings and DataCondensers.
"""

# local
from cyphon.autocomplete import AutoCompleteModelFormMixin, ChoiceWidget
from sifter.condensers.forms import (
    CondenserForm,
    FittingForm,
    FittingInlineForm,
    ParserForm
)
from .models import DataCondenser, DataFitting, DataParser


class DataParserForm(ParserForm):
    """
    Defines a form for adding or updating a LogParser using autocomplete
    fields.
    """

    class Meta(ParserForm.Meta):
        model = DataParser


class DataCondenserForm(CondenserForm):
    """
    Defines a form for adding or updating a DataCondenser using autocomplete
    fields.
    """

    class Meta(CondenserForm.Meta):
        model = DataCondenser


class DataFittingForm(FittingForm):
    """
    Defines a form for adding or updating a DataFitting using autocomplete
    fields.
    """

    class Meta(FittingForm.Meta):
        model = DataFitting
        autocomplete_names = {
            'target_field': 'FilterTargetFieldsByDataCondenser'
        }
        widgets = {
            'target_field': ChoiceWidget('FilterTargetFieldsByDataCondenser'),
        }


class DataFittingInlineForm(FittingInlineForm, AutoCompleteModelFormMixin):
    """
    Defines an inline form for adding or updating a DataFitting using
    autocomplete fields.
    """

    class Meta(FittingInlineForm.Meta):
        model = DataFitting
        widgets = {
            'target_field': ChoiceWidget('FilterTargetFieldsByBottle'),
        }
