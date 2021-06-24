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
from django.conf import settings
from django.db.models.signals import post_save

# local
from alerts.models import Alert, Analysis, Comment
from .models import DataTagger, Tag


def tag_alert(sender, instance, created, **kwargs):
    """Tag a new |Alert|."""
    DataTagger.objects.process(instance)


def tag_analysis(sender, instance, created, **kwargs):
    """Tag an |Analysis|."""
    Tag.objects.process(value=instance.notes, obj=instance)


def tag_comment(sender, instance, created, **kwargs):
    """Tag a |Comment|."""
    Tag.objects.process(value=instance.content, obj=instance)


if not settings.TEST:
    post_save.connect(tag_alert, sender=Alert)
    post_save.connect(tag_analysis, sender=Analysis)
    post_save.connect(tag_comment, sender=Comment)
