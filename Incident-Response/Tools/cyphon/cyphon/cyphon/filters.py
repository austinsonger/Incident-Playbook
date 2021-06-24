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
Defines an ObjectFilterBackend class.
"""

# third party
from django.db.models import Count, Q
from django_filters.rest_framework import DjangoFilterBackend

# local
from cyphon.relations import ModelSearchMixIn


class ObjectFilterBackend(DjangoFilterBackend, ModelSearchMixIn):
    """
    Provides a filter backend for a REST API endpoint. The backend can
    filter results for a Model using an object instance of another
    Model that may be related through a chain of forward relations.
    The backend searches the model graph for direct or indirect
    relationships between the two models, then uses the object instance
    to query for related objects.

    The backend searches for forward relationships defined by
    |ForeignKey|, |ManyToManyField|, and |OneToOneField| fields.
    It ignores reverse relations and |GenericForeignKey| fields.
    It also ignores fields and models specified by :attr:`~IGNORED_FIELDS`
    and :attr:`~IGNORED_MODELS`.

    """

    IGNORED_FIELDS = [
        ('alerts', 'Alert', 'assigned_user'),
    ]
    """
    A |list| of 3-tuples of |str| that specify the app label, model,
    and field name of |Fields| that should be ignored when searching
    the model graph for forward relations.

    """

    @staticmethod
    def _get_field_lookup(field, current_lookup):
        """
        Takes a Model field and a string for a current lookup value.
        The `current_lookup` represents a lookup for a field that
        is a forward relation to the model to which the `field` belongs.
        Returns a new lookup that spans the relationship to `field`.
        """
        if current_lookup:
            return current_lookup + '__' + field.name
        else:
            return field.name

    @staticmethod
    def _should_exclude(field):
        """
        Takes a Model field and returns a Boolean indicating whether
        the field should be used to exclude results that relate to
        objects other than that specified in the filter query.
        """
        return field.many_to_many

    def _create_lookups(self, base_model, target_model, handled_fields=None,
                        current_lookup=None):
        """
        Returns lookups for forward relations from a base model to a
        target model.

        Parameters
        ----------
        base_model : type
            The Model type representing the starting point when
            searching for paths to the `target_model` via forward
            relations.

        target_model : type
            A Model type representing the end point when searching
            for paths from the `base_model` via forward relations.

        handled_fields : `set` or `None`
            A set of Model fields that have been visited in the current
            path. Fields in this set are skipped if visited again.
            This avoids circular paths that would cause infinite
            recursions.

        current_lookup : `str` or `None`
            A lookup for the field at the current point in the path,
            starting from the `base_model`.

        Returns
        -------
        dict
            A dictionary with the keys 'filters' and 'exclude'.
            The value of 'filters' is a list of strings representing
            lookups for forward relations from the `base_model` to the
            `target model`. The value of 'exclude' is a subset of the
            `filters` list that should be used to exclude results that
            also relate to objects other than that specified in the
            filter query (e.g., ManyToManyFields that relate to both
            the specified object as well as other objects).

        Notes
        -----
        This method intentionally ignores reverse relations.

        Warning
        -------
        Currently, this method ignores forward relations defined using
        GenericForeignKey fields.

        """
        lookups = {'filters': [], 'exclude': []}
        handled_fields = handled_fields or set()

        for field in self.get_model_fields(base_model):

            field_lookup = self._get_field_lookup(field, current_lookup)

            # base case
            if self.ignore_field(field=field, ignore_reverse=True,
                                 handled_fields=handled_fields):
                continue

            # base case
            elif field.related_model == target_model:
                lookups['filters'].append(field_lookup)
                if self._should_exclude(field):
                    lookups['exclude'].append(field_lookup)

            # recursive case
            else:
                handled_fields.add(field)
                related_lookups = self._create_lookups(
                    base_model=field.related_model,
                    target_model=target_model,
                    handled_fields=handled_fields,
                    current_lookup=field_lookup
                )
                lookups['filters'].extend(related_lookups['filters'])
                if self._should_exclude(field):
                    lookups['exclude'].extend(related_lookups['filters'])
                if related_lookups['exclude']:
                    lookups['exclude'].extend(related_lookups['exclude'])

        return lookups

    def _get_lookups(self, obj, queryset):
        """
        Takes a Model object instance and a QuerySet. Returns a dict
        containing lookups used to filter and exclude records from the
        queryset.
        """
        base_model = queryset.model
        target_model = type(obj)
        return self._create_lookups(base_model, target_model)

    @staticmethod
    def _get_other_objects(obj):
        """
        Takes a Model object instance and returns a QuerySet for all
        objects except the given one.
        """
        obj_model = type(obj)
        return obj_model.objects.exclude(pk=obj.pk)

    @staticmethod
    def _apply_filter(queryset, filter_lookups, obj):
        """
        Takes a QuerySet, a list of lookup strings, and a Model object
        instance. Returns a QuerySet of records related to the object.
        """
        filter_kwargs = {}
        for filter_lookup in filter_lookups:
            filter_kwargs[filter_lookup] = obj
        return queryset.filter(**filter_kwargs)

    def _apply_exclude(self, queryset, exclude_lookups, obj):
        """
        Takes a QuerySet, a list of lookup strings, and a Model object
        instance. Returns a QuerySet of records that do not contain
        many-to-many forward relations to any object other than the
        given `obj`.
        """
        other_objects = self._get_other_objects(obj)
        exclude_kwargs = {}
        for exclude_lookup in exclude_lookups:
            exclude_kwargs[exclude_lookup + '__in'] = other_objects
        return queryset.exclude(**exclude_kwargs)

    def filter_by_object(self, obj, queryset, exclude_mixed_m2m=True):
        """Filter a queryset based on forward relations to an object.

        Parameters
        ----------
        obj : Model
            An instance of a |Model| subclass used to filter the
            `queryset`.

        queryset : QuerySet
            A |QuerySet| that should be filtered using forward relations
            to the given `obj`.

        exclude_mixed_m2m : bool
            A |bool| indicating whether the QuerySet should exclude
            records with many-to-many forward relations that are not
            exclusive to the given `obj`. This can be used to prevent
            a user from seeing objects that also relate to other users.

        Returns
        -------
        QuerySet
            A |QuerySet| containing only records with forward relations
            to `obj`. If `exclude_mixed_m2m` is |True|, the queryset
            also excludes records that relate to other objects of the
            `obj`'s type.

        Warning
        -------
        This method ignores reverse relations and relations defined
        using GenericForeignKey fields.

        """
        lookups = self._get_lookups(obj, queryset)
        filter_lookups = lookups['filters']
        exclude_lookups = lookups['exclude']

        if filter_lookups:
            queryset = self._apply_filter(queryset, filter_lookups, obj)

        if exclude_mixed_m2m and exclude_lookups:
            queryset = self._apply_exclude(queryset, exclude_lookups, obj)

        return queryset.distinct()


class GroupFilterBackend(ObjectFilterBackend):
    """
    Provides a filter backend to only show records that are either
    associated with at least one of a given user's |Group| or are not
    associated with any |Group|.
    """

    def filter_queryset(self, request, queryset, view):
        """Return a filtered queryset.

        Implements `custom filtering`_.

        Parameters
        ----------
        request : Request
            A `Request`_ for a resource.

        queryset : QuerySet
            A |QuerySet| to be filtered.

        view : ModelViewSet
            A `ModelViewSet`_.

        Returns
        -------
        QuerySet
            A |QuerySet| filtered to only show objects that are either
            associated with at least one of a given user's |Group| or
            are not associated with any |Group|.

        """
        user = request.user
        user_groups = user.groups.all()
        queryset = queryset.annotate(group_cnt=Count('groups'))
        no_groups_q = Q(group_cnt=0)
        shared_groups_q = Q(groups__in=user_groups)

        if user_groups:
            queryset = queryset.filter(no_groups_q | shared_groups_q)
        else:
            queryset = queryset.filter(no_groups_q)

        return queryset.distinct()
