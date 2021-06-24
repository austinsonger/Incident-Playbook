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
from django.contrib.contenttypes.admin import GenericTabularInline

# local
from .forms import DataTaggerForm, TagForm
from .models import DataTagger, Tag, TagRelation, Topic


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    """Customizes admin pages for |Topics|."""

    list_display = ['name', ]
    link_display = ['name', ]
    fields = ['name', ]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Customizes admin forms for |Tags|."""

    list_display = ['name', 'topic', 'article', ]
    form = TagForm


class TagRelationInlineAdmin(GenericTabularInline):
    """Customizes inline admin forms for |TagRelations|."""

    model = TagRelation
    fields = (
        'tag',
    )
    extra = 1
    verbose_name_plural = 'tags'


@admin.register(TagRelation)
class TagRelationAdmin(admin.ModelAdmin):
    """Customizes admin pages for |TagRelations|."""

    list_display = [
        'tagged_object',
        'content_type',
        'tag',
        'tagged_by',
        'tag_date',
    ]
    list_display_links = ['tagged_object', ]
    related_lookup_fields = {
        'generic': [['content_type', 'object_id'], ],
    }
    readonly_fields = ['tagged_by', 'tag_date']


@admin.register(DataTagger)
class DataTaggerAdmin(admin.ModelAdmin):
    """Customizes inline admin forms for |DataTaggers|."""

    form = DataTaggerForm
    save_as = True
