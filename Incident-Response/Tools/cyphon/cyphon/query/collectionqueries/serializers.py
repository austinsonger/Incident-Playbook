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
from rest_framework import serializers

# local
from query.collectionqueries.models import CollectionQuery, Fieldset
from warehouses.models import Collection


class FieldsetSerializer(serializers.ModelSerializer):

    class Meta(object):
        """Metadata options."""

        model = Fieldset
        fields = ['field_name', 'field_type', 'operator', 'value']


class CollectionQuerySerializer(serializers.ModelSerializer):

    # we'll specify collections using PrimaryKeys
    collections = serializers.PrimaryKeyRelatedField(
        queryset=Collection.objects.all(),
        many=True
    )

    # we'll define fieldsets using individual fields
    fieldsets = FieldsetSerializer(many=True)

    class Meta(object):
        """Metadata options."""

        model = CollectionQuery
        fields = ['collections', 'fieldsets', 'joiner']

        # values for these fields will be added automatically
        read_only_fields = ['created_by', 'created_date']

        # include fields for child objects like fieldsets
        depth = 1

    @staticmethod
    def create(validated_data):
        """
        Takes validated JSON for a field-based query and returns a CollectionQuery
        object.
        """
        # remove all ForeignKey relationships before creating the CollectionQuery
        fieldsets = validated_data.pop('fieldsets')
        collections = validated_data.pop('collections')

        # create a bare-bones CollectionQuery with the remaining fields
        query = CollectionQuery.objects.create(**validated_data)

        # add relationships to the chosen Collections
        for collection in collections:
            query.collections.add(collection)

        # create Fieldsets that are related to the CollectionQuery
        for fieldset in fieldsets:
            Fieldset.objects.create(query=query, **fieldset)

        return query
