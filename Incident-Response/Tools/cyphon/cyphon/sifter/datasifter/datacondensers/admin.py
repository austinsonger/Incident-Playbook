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
Defines a ModelAdmin subclasses for DataParsers, DataCondensers, and
DataFittings, and registers them with Django Admin.
"""

# third party
from django.contrib import admin

# local
from parsers.admin import FieldParserAdmin
from sifter.condensers.admin import (
    FittingInLineAdmin,
    FittingAdmin,
    CondenserAdmin
)
from .models import DataCondenser, DataParser, DataFitting
from .forms import (
    DataCondenserForm,
    DataFittingForm,
    DataFittingInlineForm,
    DataParserForm
)


class DataParserAdmin(FieldParserAdmin):
    """
    Customizes admin pages for DataParsers.
    """
    model = DataParser
    form = DataParserForm


class DataFittingInLineAdmin(FittingInLineAdmin):
    """
    Customizes admin inline tables for DataFittings.
    """
    model = DataFitting
    form = DataFittingInlineForm


class DataFittingAdmin(FittingAdmin):
    """
    Customizes admin pages for DataFittings.
    """
    form = DataFittingForm


class DataCondenserAdmin(CondenserAdmin):
    """
    Customizes admin pages for DataCondensers.
    """
    data_format = 'json'
    inlines = [DataFittingInLineAdmin, ]
    form = DataCondenserForm


admin.site.register(DataParser, DataParserAdmin)
admin.site.register(DataCondenser, DataCondenserAdmin)
admin.site.register(DataFitting, DataFittingAdmin)

