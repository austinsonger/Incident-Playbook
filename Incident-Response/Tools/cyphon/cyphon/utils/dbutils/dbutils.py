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
import json

# third party
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count, IntegerField, Subquery


class SQCount(Subquery):
    """A modified :class:`django.db.models.Subquery` that selects counts."""

    template = "(SELECT count(*) FROM (%(subquery)s) _count)"
    output_field = IntegerField()


def count_by_group(queryset, column, options):
    """
    Takes a QuerySet, a column name, and an options list (tuple of 2-tuples).
    Returns a dictionary containing the number of records for each option.
    """
    counts = {key: 0 for key, _ in options}
    grouped_qs = queryset.model.objects.filter(
        id__in=queryset.values(queryset.model._meta.pk.name))
    grouped_qs = grouped_qs.values(column).annotate(Count(column)).order_by()
    for result in grouped_qs:
        counts[result[column]] = result[column + '__count']
    return {column: counts}


def json_encodeable(data):
    """

    """
    serialized_data = json.dumps(data, cls=DjangoJSONEncoder)
    return json.loads(serialized_data)


def join_query(queries, logic):
    """

    """
    if logic not in ['AND', 'OR']:
        raise ValueError('%s is not a valid logic value', logic)

    joined_query = queries.pop()

    if logic == 'OR':
        for query in queries:
            joined_query |= query

    elif logic == 'AND':
        for query in queries:
            joined_query &= query

    return joined_query
