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
Defines classes for tagging objects.

======================  ================================================
Class                   Description
======================  ================================================
:class:`~DataTagger`    Assigns and creates |Tags| based on Alert data.
:class:`~Tag`           Term for describing objects.
:class:`~TagRelation`   Association between a |Tag| and an object.
======================  ================================================

"""

# standard library
import logging

# third party
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _
import nltk

# local
from articles.models import Article
from bottler.containers.models import Container
from cyphon.models import FindEnabledMixin
from taxonomies.models import Taxonomy, TaxonomyManager
from utils.parserutils.parserutils import get_dict_value
from utils.validators.validators import lowercase_validator

_LEMMATIZER = nltk.stem.WordNetLemmatizer()
_LOGGER = logging.getLogger(__name__)


try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')


class Topic(Taxonomy):
    """A category used to classify |Tags|.

    Attributes
    ----------
    name : str
        The name of the Topic.

    """

    name = models.CharField(max_length=255, unique=True)

    objects = TaxonomyManager()

    class Meta(object):
        """Metadata options."""

        ordering = ['name']


class TagManager(models.Manager):
    """Manage |Tag| objects.

    Adds methods to the default Django model manager.
    """

    @staticmethod
    def _get_tokens(value):
        """Convert a string into a set of raw and lemmatized tokens."""
        tokens = nltk.word_tokenize(value)
        tokens += [_LEMMATIZER.lemmatize(token) for token in tokens]
        return set(tokens)

    def get_by_natural_key(self, topic_name, tag_name):
        """Get a |Tag| by its natural key.

        Allows retrieval of a |Tag| by its natural key instead of
        its primary key.

        Parameters
        ----------
        name : |str|
            The name of the |Tag| associated with the |Tag|.

        topic : |str|
            The name of the |Topic| associated with the |Tag|.

        Returns
        -------
        |Tag|
            The |Tag| associated with the natural key.

        """
        topic = Topic.objects.get_by_natural_key(name=topic_name)
        if topic:
            return self.get(name=tag_name, topic=topic.pk)
        else:
            _LOGGER.error('The Tag %s:%s does not exist', tag_name, topic_name)

    def process(self, value, obj, queryset=None, user=None):
        """Tag an object.

        Parameters
        ----------

        value : |str|
            A string to be matched against the `queryset`.

        obj : |Alert| or |Comment|
            The object to to be tagged.

        queryset : |QuerySet| of |Tags|
            The |Tags| that should be included in the analysis. If set
            to |None|, all |Tags| will be used.

        user : |AppUser|
            The user tagging the object. Default is |None|.

        Returns
        -------
        |TagRelation|

        """
        if queryset is None:
            queryset = self.get_queryset()

        tokens = self._get_tokens(value)

        for tag in queryset:
            tag_tokens = nltk.word_tokenize(tag.name)
            if (len(tag_tokens) > 1):
                contains_tag = tag.name in value
            else:
                contains_tag = tag.name in tokens
            if contains_tag:
                tag.assign_tag(obj)


class Tag(models.Model):
    """A term for describing objects.

    Attributes
    ----------
    name : str
        The name of the Tag.

    topic : Topic
        The |topic| to which the Tag relates.

    article : Article
        The |Article| about the Tag.

    """

    name = models.CharField(
        max_length=255,
        validators=[lowercase_validator],
        help_text=_('Tags must be lowercase.')
    )
    topic = models.ForeignKey(
        Topic,
        blank=True,
        null=True,
        related_name='tags',
        related_query_name='tag'
    )
    article = models.ForeignKey(
        Article,
        blank=True,
        null=True,
        related_name='tags',
        related_query_name='tag'
    )

    objects = TagManager()

    class Meta(object):
        """Metadata options."""

        ordering = ['topic', 'name']
        unique_together = ['name', 'topic']

    def __str__(self):
        """Return a string representation of the Tag."""
        return self.name

    def assign_tag(self, obj, user=None):
        """Associate a tag with an object.

        Parameters
        ----------
        obj : |Alert| or |Comment|
            The object to be tagged.

        user : |AppUser|
            The user tagging the object.

        Returns
        -------
        |TagRelation|

        """
        model_type = ContentType.objects.get_for_model(obj)
        (tag_relation, dummy_created) = TagRelation.objects.get_or_create(
            content_type=model_type,
            object_id=obj.pk,
            tag=self,
            tagged_by=user
        )
        return tag_relation


class TagRelation(models.Model):
    """Association between a |Tag| and an object.

    Attributes
    ----------
    content_type : ContentType
        The |ContentType| of object that was tagged.

    object_id : int
        The id of the :attr:`~TagRelation.tagged_object`.

    tagged_object : `Alert` or `Comment`
        The object that was tagged, which can be an |Alert|, |Analysis|,
        or |Comment|.

    tag : Tag
        The |Tag| associated with the :attr:`~TagRelation.tagged_object`.

    tag_date : datetime
        The |datetime| when the TagRelation was created.

    tagged_by : AppUser
        The |AppUser| who created the TagRelation.

    """

    _ALERT = models.Q(app_label='alerts', model='alert')
    _ANALYSIS = models.Q(app_label='alerts', model='analysis')
    _COMMENT = models.Q(app_label='alerts', model='comment')
    _TAGGED = _ALERT | _ANALYSIS | _COMMENT

    content_type = models.ForeignKey(
        ContentType,
        limit_choices_to=_TAGGED,
        blank=True,
        null=True,
        on_delete=models.PROTECT
    )
    object_id = models.PositiveIntegerField(blank=True, null=True)
    tagged_object = GenericForeignKey('content_type', 'object_id')
    tag = models.ForeignKey(
        Tag,
        related_name='tag_relations',
        related_query_name='tag_relations'
    )
    tag_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    tagged_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.PROTECT
    )

    class Meta(object):
        """Metadata options."""

        unique_together = ('content_type', 'object_id', 'tag')

    def __str__(self):
        """Return a string representation of the TagRelation."""
        return '%s <%s: %s>' % (self.tag, str(self.content_type).title(),
                                self.tagged_object)


class DataTaggerManager(models.Manager, FindEnabledMixin):
    """Manage |DataTagger| objects.

    Adds methods to the default Django model manager.
    """

    def process(self, alert):
        """Tag an |Alert|.

        Parameters
        ----------
        alert : |Alert|
            The |Alert| to be tagged.

        Returns
        -------
        None

        """
        for datatagger in self.find_enabled():
            datatagger.process(alert)


class DataTagger(models.Model):
    """Tags an |Alert| based on the value of a Container field.

    Attributes
    ----------
    container : Container
        The |Container| associated with the field to be inspected.

    field_name : str
        The name of the field to be inspected.

    topics : `QuerySet` of `Topics`
        |Topics| for |Tags| that should be used to analyze the field.

    exact_match : bool
        Whether the value of the field must exactly match a |Tag|.

    create_tags : bool
        Whether a |Tag| should be created from the value of a field.
        If |True|, create news |Tags| under the |Topic| defined by
        :attr:`DataTagger.default_topic`.

    enabled : bool
        Whether the DataTagger is enabled.

    """
    container = models.ForeignKey(Container)
    field_name = models.CharField(
        max_length=255,
        help_text=_('The name of the Container field that should be analyzed '
                    'for tagging. Use dot notation to indicate nested fields '
                    '(e.g., "user.name").')
    )
    topics = models.ManyToManyField(
        Topic,
        help_text=_('Restrict tagging to these topics. '
                    'If none are selected, all topics will be included '
                    'in the analysis.')
    )
    exact_match = models.BooleanField(
        default=False,
        help_text=_('Match the entire content of the field. If checked, '
                    'please select one and only one tag topic for '
                    'analyzing this field.')
    )
    create_tags = models.BooleanField(
        default=False,
        help_text=_('Create new tags from this field '
                    '(only available when using exact match).')
    )
    enabled = models.BooleanField(default=True)

    objects = DataTaggerManager()

    class Meta(object):
        """Metadata options."""

        ordering = ['container', 'field_name']
        unique_together = ['container', 'field_name']

    def __str__(self):
        """Return a string representation of the DataTagger."""
        return '%s: %s' % (self.container, self.field_name)

    def _get_value(self, alert):
        """Return a lowercase string from an Alert's data field."""
        value = get_dict_value(self.field_name, alert.data)
        if isinstance(value, str):
            return value.lower()

    def _create_tag(self, tag_name):
        """Create a new Tag from a tag_name."""
        try:
            topic = self.topics.all()[0]
            (tag, dummy_created) = Tag.objects.get_or_create(name=tag_name,
                                                             topic=topic)
            return tag
        except (IndexError, ValidationError) as error:
            _LOGGER.error('An error occurred while creating '
                          'a new tag "%s": %s', tag_name, error)

    def _get_relevant_tags(self):
        """Return a QuerySet of Tags to include in the analysis.

        If the DataTagger is associated with particular Topics, only
        returns Tags belonging to those Topics. Otherwise, returns
        all Tags.
        """
        topics = self.topics.all()
        if topics:
            return Tag.objects.filter(topic__in=topics)
        else:
            return Tag.objects.all()

    def _get_tag(self, tag_name):
        """Return a Tag with the given tag name.

        If the Tag does not already exist, creates the Tag if
        self.create_tags is True.
        """
        try:
            topic = self.topics.all()[0]
            return Tag.objects.get(name=tag_name, topic=topic)
        except (IndexError, ObjectDoesNotExist):
            if self.create_tags:
                return self._create_tag(tag_name)

    def _tag_exact_match(self, alert, value):
        """Assign a Tag to an Alert based on an exact match."""
        tag = self._get_tag(value)
        if tag:
            tag.assign_tag(alert)

    def _tag_partial_match(self, alert, value):
        """Assign a Tag to an Alert based on a partial match.

        If a Tag contains more than one token, matches the Tag against
        the raw field value. Otherwise, matches the Tag against a list
        of tokens created from the field value.
        """
        tags = self._get_relevant_tags()
        Tag.objects.process(value, alert, tags)

    def process(self, alert):
        """Assign |Tags| to an |Alert| based on a |Container| field.

        Parameters
        ----------
        alert : |Alert|
            An |Alert| to be tagged.

        Returns
        -------
        None

        """
        value = self._get_value(alert)
        if value:
            if self.exact_match:
                self._tag_exact_match(alert, value)
            else:
                self._tag_partial_match(alert, value)
