# -*- coding: utf-8 -*-
# Copyright 2017 ControlScan.
#
# This file is part of Cyphon Engine.
#
# Cyphon Engine is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
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
import logging

# third party
from ckeditor_uploader.fields import RichTextUploadingField
from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

_LOGGER = logging.getLogger(__name__)


class ArticleManager(models.Manager):
    """Adds methods to the default model manager."""

    def get_by_natural_key(self, title):
        """Get an |Article| by its `title`.

        Parameters
        ----------
        title : str
            The Article's `title`.

        Returns
        -------
        |Article|
            The |Article| with the specified `title`.

        """
        try:
            return self.get(title=title)
        except ObjectDoesNotExist:
            logging.getLogger(self.__module__).error('%s "%s" does not exist',
                                                     self.model.__name__, title)


class Article(models.Model):
    """A reference article.

    Attributes
    ----------
    title : str
        The title of the Article.

    content : str
        The Article content.

    """

    title = models.CharField(
        unique=True,
        max_length=255,
    )
    content = RichTextUploadingField()

    objects = ArticleManager()

    class Meta(object):
        """Metadata options."""

        ordering = ['title']

    def __str__(self):
        """Return a string representation of the Article."""
        return self.title

    @property
    def topics(self):
        """Get |Topics| associated with the Article.

        Returns
        -------
        |QuerySet| of |Topics|
            The |Topics| associated with the Article's |Tags|.

        """
        # use get_model to avoid circular dependency
        topic_model = apps.get_model('tags', 'Topic')
        return topic_model.objects.filter(tag__in=self.tags.all()).distinct()
