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
Defines serializers for |Distilleries|.

====================================  ========================================
Class                                 Description
====================================  ========================================
:class:`~ArticleSerializer`           Serializer for |Article| views.
====================================  ========================================

"""

# third party
from rest_framework import serializers

# local
from tags.serializers import TagListSerializer, TopicSerializer
from .models import Article


class ArticleDetailSerializer(serializers.ModelSerializer):
    """Serializer for a |Article| objects."""

    topics = TopicSerializer(many=True)
    tags = TagListSerializer(many=True)

    class Meta(object):
        """Metadata options."""

        model = Article
        depth = 2
        fields = (
            'id',
            'title',
            'content',
            'topics',
            'tags',
        )


class ArticleListSerializer(serializers.ModelSerializer):
    """Serializer for a |Article| objects."""

    class Meta(object):
        """Metadata options."""

        model = Article
        fields = (
            'id',
            'title',
            'url',
        )
