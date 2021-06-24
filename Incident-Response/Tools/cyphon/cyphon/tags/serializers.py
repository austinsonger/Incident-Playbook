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
:class:`~TagSerializer`               Serializer for |Tag| views.
:class:`~TopicSerializer`             Serializer for |Topic| views.
====================================  ========================================

"""

# third party
from rest_framework import serializers

# local
from articles.models import Article
from .models import Tag, Topic


class ArticleSerializer(serializers.ModelSerializer):
    """Serializer for a |Article| objects."""

    class Meta(object):
        """Metadata options."""

        model = Article
        fields = (
            'id',
            'title',
            'url',
        )


class TopicSerializer(serializers.ModelSerializer):
    """Serializer for |Topic| objects."""

    class Meta(object):
        """Metadata options."""

        model = Topic
        fields = (
            'id',
            'name',
            'url'
        )


class TagDetailSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for a |Tag| object."""

    topic = TopicSerializer()
    article = ArticleSerializer()

    class Meta(object):
        """Metadata options."""

        model = Tag
        fields = (
            'id',
            'name',
            'topic',
            'article',
        )


class TagListSerializer(serializers.ModelSerializer):
    """Serializer for a list of |Tag| objects."""

    class Meta(object):
        """Metadata options."""

        model = Tag
        fields = (
            'id',
            'name',
        )
