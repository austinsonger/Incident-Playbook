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
Forms for selecting a Warehouse and constructing a database query.
"""

# third party
from django import forms

# local
from distilleries.models import Distillery
from warehouses.models import Collection


class CollectionSelectForm(forms.Form):
    """
    Form for selecting a Collection (database collection) on which to perform
    a query.
    """
    collection = forms.ModelChoiceField(queryset=None)

    def __init__(self, *args, **kwargs):
        collection = kwargs.pop('collection', None)
        super(CollectionSelectForm, self).__init__(*args, **kwargs)

        # provide an option to use a filtered queryset, if, for instance,
        # we want to check a user's permissions to access specific collections
        if collection:
            queryset = kwargs['collections']
        else:
            queryset = Collection.objects.all()

        self.fields['collection'].queryset = queryset


class CollectionQueryForm(forms.Form):
    """
    Form for creating a query for a specific database collection.
    """
    datafield = forms.ChoiceField()
    operator = forms.ChoiceField()
    value = forms.CharField()

    def __init__(self, *args, **kwargs):
        name = kwargs.pop('name', None)
        super(CollectionQueryForm, self).__init__(*args, **kwargs)

        if name:

            # TODO(LH): provide contingency if no Distillery is associated with
            # the warehouse
            distillery = Distillery.objects.get_by_natural_key(name)
            field_choices = self._get_field_choices(distillery.bottle)
            operator_choices = self._get_operator_choices()

            self.fields['datafield'] = forms.ChoiceField(
                choices=field_choices,
                label='Field name',
                widget=forms.Select(
                    attrs={'class': 'field'},
                )
            )

            self.fields['operator'] = forms.ChoiceField(
                choices=operator_choices,
                widget=forms.Select(
                    attrs={'class': 'operator'},
                )
            )

            self.fields['value'] = forms.CharField(
                required=False,
                widget=forms.TextInput(
                    attrs={'class': 'value'},
                )
            )

    @staticmethod
    def _get_field_choices(bottle):
        """
        Takes a Bottle and adds choices to the datafield ChoiceField
        based on the fields used in the Warehouse.
        """
        default_choice = ('', '-- select a field --')
        field_choices = bottle.get_field_choices()

        choices = [default_choice]
        choices.extend(field_choices)

        return choices

    @staticmethod
    def _get_operator_choices():
        """
        Returns a tuple of 2-tuples representing valid choices for the query
        operator field.
        """
        return (

            # BooleanField choices
            ('eq', 'is true'),
            ('not:eq', 'is false'),

            # DateTimeField choices
            ('gte', 'occurred on or after'),
            ('lte', 'occurred on or before'),

            # default options
            ('eq', 'equals'),
            ('not:eq', 'does not equal'),

            # ListField choices
            ('in', 'contains'),
            ('not:in', 'does not contain'),

            # FloatField or IntegerField options
            ('eq', 'equals'),
            ('ne', 'does not equal'),
            ('gt', 'greater than'),
            ('gte', 'greater than or equal to'),
            ('lt', 'less than'),
            ('lte', 'less than or equal to'),

            # CharField options
            ('regex', 'contains'),
            ('eq', 'equals'),
            ('not:regex', 'does not contain'),

            # just used in test cases for $not
            ('not:eq', 'does not equal'),
        )


class JoinOperatorForm(forms.Form):
    """
    Defines a form for specifiying whether query terms should be joined with an
    'AND' or 'OR' operator.
    """
    JOIN_CHOICES = (
        ('AND', 'satisfy all filter conditions'),
        ('OR', 'satisfy at least one filter condition')
    )

    joiner = forms.ChoiceField(choices=JOIN_CHOICES, label='Query type')
