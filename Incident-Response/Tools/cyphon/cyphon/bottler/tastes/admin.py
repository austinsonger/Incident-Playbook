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

# third party
from django.contrib import admin

# local
from .forms import TasteForm, TasteInlineForm
from .models import Taste


class TasteAdmin(admin.ModelAdmin):
    """
    Customizes the admin page for Tastes.
    """
    model = Taste
    form = TasteForm


class TasteInLineAdmin(admin.StackedInline):
    """
    Customizes inline admin forms for Tastes.
    """
    model = Taste
    form = TasteInlineForm
    classes = ('grp-open', )
    inline_classes = ('grp-open', )
    max_num = 1
    min_num = 1
    verbose_name_plural = 'taste'
    can_delete = False


admin.site.register(Taste, TasteAdmin)

