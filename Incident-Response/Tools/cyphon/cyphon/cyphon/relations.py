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
from django.contrib.contenttypes.fields import GenericRelation
from django.db.models.fields.reverse_related import ForeignObjectRel
from django.apps import apps


class ModelSearchMixIn(object):
    """


    """

    IGNORED_FIELDS = []
    """
    A |list| of 3-tuples of |str| that specify the app label, model,
    and field name of |Fields| that should be ignored when searching
    the model graph for forward relations.

    """

    IGNORED_MODELS = [
        ('auth', 'Group'),
        ('auth', 'Permission'),
        ('contenttypes', 'ContentType'),
    ]
    """
    A |list| of 2-tuples of |str| that specify the app label and
    model of |Models| that should be ignored when searching the
    model graph for forward relations.

    """

    @staticmethod
    def get_model_key(model):
        """

        """
        app_label = model._meta.app_label
        model_name = model.__name__
        return (app_label, model_name)

    @staticmethod
    def get_models(model_keys):
        """

        """
        return [apps.get_model(*args) for args in model_keys]

    @property
    def ignored_models(self):
        """
        Returns a list of Models that should be ignored when searching
        the model graph for forward relations.
        """
        return self.get_models(self.IGNORED_MODELS)

    @property
    def ignored_fields(self):
        """
        Returns a list of Fields that should be ignored when searching
        the model graph for forward relations.
        """
        ignored_fields = []
        for args in self.IGNORED_FIELDS:
            model = apps.get_model(args[0], args[1])
            field = model._meta.get_field(args[2])
            ignored_fields.append(field)
        return ignored_fields

    @staticmethod
    def field_is_reverse_relation(field):
        """
        Takes a Model field and returns a Boolean indicating whether
        the field refers to a reverse relation.
        """
        reverse_relations = (ForeignObjectRel, GenericRelation, )
        return isinstance(field, reverse_relations)

    def ignore_field(self, field, ignore_reverse, handled_fields):
        """
        Takes a Model field and a list of Model fields that have already
        been examined. Returns a Boolean indicating whether the field
        should be ignored when creating lookups.

        Returns True if any of the following are True:
            - the field does not have a related model
            - the field has already been processed
            - the field is in IGNORED_FIELDS
            - the field's related model is in IGNORED_MODELS
            - the field is a reverse relation

        """
        return not field.related_model \
            or field in handled_fields \
            or field in self.ignored_fields \
            or field.related_model in self.ignored_models \
            or (ignore_reverse and self.field_is_reverse_relation(field))

    @staticmethod
    def get_model_fields(model):
        """
        Takes a Model type and returns a tuple of fields associated
        with it.
        """
        return model._meta.get_fields(include_parents=True,
                                      include_hidden=False)

    def is_related(self, base_model, target_models, ignore_reverse,
                   handled_fields=None):
        """

        """
        is_related = False
        handled_fields = handled_fields or set()

        # base case
        if base_model in target_models:
            return True

        # recursive case
        else:
            for field in self.get_model_fields(base_model):

                if self.ignore_field(field, ignore_reverse, handled_fields):
                    continue

                else:
                    handled_fields.add(field)
                    is_related |= self.is_related(
                        base_model=field.related_model,
                        target_models=target_models,
                        ignore_reverse=ignore_reverse,
                        handled_fields=handled_fields
                    )

        return is_related

