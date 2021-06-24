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
Forms for selecting a Tags and DataTaggers.
"""

# third party
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

# local
from .models import DataTagger, Tag


class TagForm(forms.ModelForm):
    """
    Form for creating a |Tag|.
    """

    class Meta(object):
        """Metadata options."""

        model = Tag
        exclude = []

    def clean_name(self):
        """Validate the name field."""
        name = self.cleaned_data['name']
        return name.lower()


class DataTaggerForm(forms.ModelForm):
    """
    Form for creating a |DataTagger|.
    """

    class Meta(object):
        """Metadata options."""

        model = DataTagger
        exclude = []

    def clean(self):
        """Validate the model as a whole.

        Returns
        -------
        None

        Raises
        ------
        ValidationError
            If the `field_name` does not represent a field in the
            `container`, or if `exact_match` is |True| and zero or
            multiple `topics` are selected, or if `create_tags` is
            |True| but `exact_match` is |False|.

        See also
        --------
        See Django's documentation for the
        :meth:`~django.db.models.Model.clean` method.

        """
        cleaned_data = super(DataTaggerForm, self).clean()
        container = cleaned_data.get('container')
        field_name = cleaned_data.get('field_name')
        exact_match = cleaned_data.get('exact_match')
        create_tags = cleaned_data.get('create_tags')
        topics = cleaned_data.get('topics')

        if field_name not in container.get_field_list():
            raise ValidationError(_('The given field name does not '
                                    'appear in the selected Container.'))

        if exact_match and (topics is None or topics.count() != 1):
            raise ValidationError(_('Select exactly one tag topic when using '
                                    'exact matches.'))

        if create_tags and not exact_match:
            raise ValidationError(_('The "create tags" feature is only '
                                    'available for exact matches.'))

        return cleaned_data
