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
Defines Alert class.
"""

# standard library
import hashlib
import json
import logging
import urllib
import uuid
import time

# third party
from ckeditor_uploader.fields import RichTextUploadingField
import dateutil.parser
from django.apps import apps
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.gis.db.models import PointField
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.forms import fields
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

# local
from cyphon.choices import (
    ALERT_LEVEL_CHOICES,
    ALERT_STATUS_CHOICES,
    ALERT_OUTCOME_CHOICES,
)
from distilleries.models import Distillery
from tags.models import Tag, TagRelation
from utils.dateutils.dateutils import convert_time_to_seconds
from utils.dbutils.dbutils import json_encodeable
from utils.parserutils.parserutils import (
    abridge_dict,
    format_fields,
    get_dict_value
)

_ALERT_URL = '/app/alerts/'

_PRIVATE_FIELD_SETTINGS = settings.PRIVATE_FIELDS

_LOGGER = logging.getLogger(__name__)


# allow parsing of ISO8601 datetime strings
fields.DateTimeField.strptime = lambda o, v, f: \
                                dateutil.parser.parse(v)  # pragma: no cover


class AlertManager(models.Manager):
    """
    Adds methods to the default model manager.
    """

    def with_codebooks(self):
        """
        Overrides the default get_queryset method to select the related
        Distillery and AppUser.
        """
        default_queryset = self.get_queryset()
        return default_queryset.select_related('distillery__company__codebook')\
               .prefetch_related('distillery__company__codebook__codenames')

    @staticmethod
    def _filter_by_group(user, queryset):
        """

        """
        user_groups = user.groups.all()
        Monitor = apps.get_model('monitors', 'Monitor')
        Watchdog = apps.get_model('watchdogs', 'Watchdog')
        monitors = models.Subquery(Monitor.objects
            .annotate(models.Count('groups'))
            .filter(models.Q(groups__count=0) |
                    models.Q(groups__in=user_groups))
            .values('id'))
        watchdogs = models.Subquery(Watchdog.objects
            .annotate(models.Count('groups'))
            .filter(models.Q(groups__count=0) |
                    models.Q(groups__in=user_groups))
            .values('id'))
        return queryset.filter(
            models.Q(watchdog__isnull=True, monitor__isnull=True) |
            models.Q(watchdog__in=watchdogs) |
            models.Q(monitor__in=monitors)).distinct()

    @staticmethod
    def _filter_by_company(user, queryset):
        """

        """
        if not user.is_staff:
            query = models.Q(distillery__company=user.company) | \
                    models.Q(distillery__company__isnull=True)
            return queryset.filter(query).distinct()
        else:
            return queryset

    def filter_by_user(self, user, queryset=None):
        """
        queryset : None or QuerySet of Alerts
        """
        if queryset is not None:
            alert_qs = queryset
        else:
            alert_qs = self.get_queryset()

        if user:
            filtered_qs = self._filter_by_company(user, alert_qs)
            return self._filter_by_group(user, filtered_qs)
        else:
            return alert_qs.none()


class Alert(models.Model):
    """
    An alert incident.

    Attributes
    ----------

    level : str
        The priority of the Alert. Options are constrained to
        :const:`~cyphon.choices.ALERT_LEVEL_CHOICES`.

    status : str
        The status of the Alert. Options are constrained to
        :const:`~cyphon.choices.ALERT_STATUS_CHOICES`.

    outcome : str
        The outcome of the Alert. Options are constrained to
        :const:`~cyphon.choices.ALERT_OUTCOME_CHOICES`.

    created_date : datetime
        The date and time the Alert was created.

    content_date : datetime
        The date and time the data that triggered the Alert was created.

    last_updated : datetime
        The date and time the Alert was last modified.

    assigned_user : AppUser
        The |AppUser| assigned to the Alert.

    alarm_type : ContentType
        The type of |Alarm| that triggered the Alert.

    alarm_id : int
        The |Alarm| object id of the |Alarm| that triggered the Alert.

    alarm : Alarm
        The |Alarm| object that generated the |Alert|, such as a |Watchdog| or
        |Monitor|.

    distillery : Distillery
        The |Distillery| associated with teh data that triggered
        the Alert.

    doc_id :  str
        The id of the document that triggered the Alert.

    data : dict
        The document that triggered the Alert.

    location : `list` of `float`
        The longitude and latitude of the location associated with
        the Alert.

    title : str
        A title describing the nature of the Alert.

    incidents : int
        The number of duplicate incidents associated with the Alert.

    tag_relations : QuerySet of TagRelations
        TagRelations associated with the Alert.

    muzzle_hash : str
        If the Alert was generated by a |Watchdog| with an enabled
        |Muzzle|, represents a hash computed from characteristics
        of the |Muzzle| and the Alert. Otherwise, consists of a UUID.
        Used to identify duplicate Alerts.

    """
    _WATCHDOG = models.Q(app_label='watchdogs', model='watchdog')
    _MONITOR = models.Q(app_label='monitors', model='monitor')
    _ALARMS = _WATCHDOG | _MONITOR

    _DEFAULT_TITLE = 'No title available'
    _HASH_FORMAT = ('{level}|{distillery}|{alarm_type}'
                    '|{alarm_id}|{field_values}|{bucket:.0f}')

    level = models.CharField(
        max_length=20,
        choices=ALERT_LEVEL_CHOICES,
        db_index=True
    )
    status = models.CharField(
        max_length=20,
        choices=ALERT_STATUS_CHOICES,
        default='NEW',
        db_index=True
    )
    outcome = models.CharField(
        max_length=20,
        choices=ALERT_OUTCOME_CHOICES,
        null=True,
        blank=True,
        db_index=True
    )
    created_date = models.DateTimeField(default=timezone.now, db_index=True)
    content_date = models.DateTimeField(blank=True, null=True, db_index=True)
    last_updated = models.DateTimeField(auto_now=True, blank=True, null=True)
    assigned_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.PROTECT
    )
    alarm_type = models.ForeignKey(
        ContentType,
        limit_choices_to=_ALARMS,
        blank=True,
        null=True,
        on_delete=models.PROTECT
    )
    alarm_id = models.PositiveIntegerField(blank=True, null=True)
    alarm = GenericForeignKey('alarm_type', 'alarm_id')
    distillery = models.ForeignKey(
        Distillery,
        blank=True,
        null=True,
        related_name='alerts',
        related_query_name='alerts',
        db_index=True,
        on_delete=models.PROTECT
    )
    doc_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        db_index=True
    )
    data = JSONField(blank=True, null=True, default=dict)
    location = PointField(blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    incidents = models.PositiveIntegerField(default=1)
    tag_relations = GenericRelation(TagRelation, related_query_name='alerts')
    muzzle_hash = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        db_index=True,
        unique=True
    )

    objects = AlertManager()

    class Meta(object):
        """Metadata options."""

        permissions = (
            ('view_alert', 'Can see existing alerts'),
        )
        ordering = ['-id']

    def __str__(self):
        if self.title:
            return 'PK %s: %s' % (self.pk, self.title)
        elif self.pk:
            return 'PK %s' % self.pk
        else:
            return super(Alert, self).__str__()

    def save(self, *args, **kwargs):
        """
        Overrides the save() method to assign a title, content_date,
        location, and data to a new Alert.
        """
        if not self.data:
            self._add_data()

        if not self.location:
            self._add_location()

        if not self.content_date:
            self._add_content_date()

        if not self.title or self.title == self._DEFAULT_TITLE:
            self.title = self._format_title()

        # set the created_date now so it can be used to create the muzzle_hash
        if not self.created_date:
            self.created_date = timezone.now()

        self.muzzle_hash = self._get_muzzle_hash()

        return super(Alert, self).save(*args, **kwargs)

    @property
    def link(self):
        """

        """
        base_url = settings.BASE_URL
        return urllib.parse.urljoin(base_url, _ALERT_URL + str(self.id))

    @property
    def coordinates(self):
        """

        """
        if self.location:
            return json.loads(self.location.json)

    @property
    def notes(self):
        """

        """
        if hasattr(self, 'analysis'):
            return self.analysis.notes

    def _add_content_date(self):
        """
        Adds a content_date from the teaser's date if it exists.
        """
        self.content_date = self.teaser.get('date')

    def _add_data(self):
        """

        """
        self.data = json_encodeable(self.saved_data)

    def _add_location(self):
        """
        Adds a location if the Alert has one.
        """
        self.location = self.teaser.get('location')

    def _get_muzzle(self):
        """
        Get the Muzzle associated with an Alert, if one exists.
        """
        if (self.alarm and hasattr(self.alarm, 'muzzle') and
                self.alarm.muzzle.enabled):
            return self.alarm.muzzle

    def _get_bucket(self, muzzle):
        """
        Get the time bucket associated with an Alert and a given Muzzle.
        """
        total_seconds = time.mktime(self.created_date.timetuple())
        interval_seconds = convert_time_to_seconds(
            muzzle.time_interval,
            muzzle.time_unit
        )

        return total_seconds // interval_seconds

    def _get_field_values(self, muzzle):
        """
        Get a string of field names and field values associated with the
        Muzzle of the Watchdog that created the Alert.
        """
        field_values = [
            ':'.join((field, get_dict_value(field, self.data) or ''))
            for field in sorted(muzzle.get_fields())
        ]
        return ','.join(field_values)

    def _get_muzzle_hash(self):
        """
        Return a muzzle_hash for the Alert.
        """
        muzzle = self._get_muzzle()
        if muzzle:
            time_bucket = self._get_bucket(muzzle)
            field_values = self._get_field_values(muzzle)
            updated_hash = hashlib.sha256(
                self._HASH_FORMAT.format(
                    level=self.level,
                    distillery=self.distillery,
                    alarm_type=self.alarm_type,
                    alarm_id=self.alarm_id,
                    field_values=field_values,
                    bucket=time_bucket
                ).encode()).hexdigest()

            # if the alert is being updated, only use the updated hash
            # if it doesn't match that of another alert
            if not (self.pk and
                    updated_hash != self.muzzle_hash and
                    Alert.objects.filter(muzzle_hash=updated_hash).exists()):
                return updated_hash

        return hashlib.sha256(uuid.uuid4().bytes).hexdigest()

    def _get_codebook(self):
        """
        Returns the Codebook for the Distillery associated with the Alert.
        """
        if self.distillery:
            return self.distillery.codebook

    def _format_title(self):
        """
        If the Alert's teaser has title defined, returns the title.
        If not, returns an empty string.
        """
        title = self.teaser.get('title', '')
        max_length = Alert._meta.get_field('title').max_length
        if title and len(title) > max_length:
            return title[:max_length]
        return title

    def _get_schema(self):
        """
        Returns a list of DataFields in the Container associated with
        the Alert's data.
        """
        if self.distillery:
            return self.distillery.schema

    def _summarize(self, include_empty=False):
        """

        """
        source_data = self.get_public_data_str()

        field_data = [
            ('Alert ID', self.id),
            ('Title', self.title),
            ('Level', self.level),
            ('Incidents', self.incidents),
            ('Created date', self.created_date),
            ('\nCollection', self.distillery),
            ('Document ID', self.doc_id),
            ('Source Data', '\n' + source_data),
            ('\nNotes', '\n' + str(self.notes)),
        ]

        return format_fields(field_data, include_empty=include_empty)

    def _summarize_with_comments(self, include_empty=False):
        """

        """
        summary = self._summarize(include_empty=include_empty)

        separator = '\n\n'
        division = '-----'

        if self.comments.count() > 0:
            summary += separator
            summary += division
            for comment in self.comments.all():
                summary += separator
                summary += comment.summary()

        return summary

    def display_title(self):
        """
        Return the Alert's title or a default title.
        """
        return self.title or self._DEFAULT_TITLE

    display_title.short_description = _('title')

    def redacted_title(self):
        """
        Return a redacted version of the Alert's title or a default title.
        """
        codebook = self._get_codebook()
        if self.title and codebook:
            return codebook.redact(self.title)
        else:
            return self.display_title()

    @cached_property
    def company(self):
        """
        Returns the Company associated with the Alert's Distillery.
        """
        if self.distillery:
            return self.distillery.company

    @property
    def saved_data(self):
        """
        Attempts to locate the document which triggered the Alert.
        If successful, returns a data dictionary of the document.
        If not, returns an empty dictionary.
        """
        has_setting = hasattr(settings, 'ALERTS')

        if has_setting and settings.ALERTS.get('DISABLE_COLLECTION_SEARCH'):
            return {}

        if self.distillery and self.doc_id:
            data = self.distillery.find_by_id(self.doc_id)
            if data:
                return data
            else:
                _LOGGER.warning('The document associated with id %s cannot be ' \
                                + 'found in %s.', self.doc_id, self.distillery)
        return {}

    @property
    def tidy_data(self):
        """
        If the Alert's data is associated with a Container, returns a
        dictionary of the Alert's data containing only the fields
        in the Container. Otherwise, returns the Alert's data.
        """
        schema = self._get_schema()
        if schema:
            return abridge_dict(schema, self.data)
        else:
            return self.data

    def get_data_str(self):
        """
        Returns the Alert data as a pretty-print string.
        """
        return json.dumps(self.data, sort_keys=True, indent=4)

    get_data_str.short_description = 'data'

    def get_public_data_str(self):
        """
        Returns the Alert data as a pretty-print string, with private
        fields removed.
        """
        public_data = {}
        for (key, val) in self.data.items():
            if key not in _PRIVATE_FIELD_SETTINGS:
                public_data[key] = val
        return json.dumps(public_data, sort_keys=True, indent=4)

    @cached_property
    def teaser(self):
        """
        Returns a Taste representing teaser data for the document which
        generated the Alert.
        """
        if self.distillery:
            return self.distillery.get_sample(self.data)
        else:
            return {}

    @property
    def associated_tags(self):
        """
        Returns a QuerySet of Tags associated with the Alert or its comments.
        """
        comment_ids = self.comments.all().values_list('id', flat=True)
        alert_relations = models.Q(
            content_type=ContentType.objects.get_for_model(Alert),
            object_id=self.id
        )
        analysis_relations = models.Q(
            content_type=ContentType.objects.get_for_model(Analysis),
            object_id=self.id
        )
        comment_relations = models.Q(
            content_type=ContentType.objects.get_for_model(Comment),
            object_id__in=comment_ids
        )
        query = alert_relations | analysis_relations | comment_relations
        tag_relations = TagRelation.objects.filter(query)
        return Tag.objects.filter(tag_relations__in=tag_relations).distinct()

    def add_incident(self):
        """
        Increments the number of incidents associated with the Alert.
        """
        # using F instead of += increments the value using a SQL query
        # and avoids race conditions
        self.incidents = models.F('incidents') + 1
        self.save()

    def summary(self, include_empty=False, include_comments=False):
        """

        """
        if include_comments:
            return self._summarize_with_comments(include_empty=include_empty)
        else:
            return self._summarize(include_empty=include_empty)


class AnalysisManager(models.Manager):
    """
    Adds methods to the default model manager.
    """

    def get_queryset(self):
        """
        Overrides the default get_queryset method to select related objects.
        """
        default_queryset = super(AnalysisManager, self).get_queryset()
        return default_queryset.select_related()

    def save_notes(self, alert, notes):
        """Create or update an |Analysis| for an |Alert|.

        Parameters
        ----------
        alert : |Alert|
            The |Alert| with which the |Analysis| is related.

        notes : str
            Notes to add to the |Analysis|.

        Returns
        -------
        |Analysis|

        """
        (analysis, dummy_created) = self.get_or_create(alert=alert)
        analysis.notes = notes
        analysis.save()
        return analysis


class Analysis(models.Model):
    """
    Analysis for an Alert.
    """
    alert = models.OneToOneField(Alert, primary_key=True)
    created_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True, blank=True, null=True)
    notes = RichTextUploadingField(blank=True)
    tag_relations = GenericRelation(TagRelation, related_query_name='analyses')

    objects = AnalysisManager()

    class Meta(object):
        """Metadata options."""

        permissions = (
            ('view_alert', 'Can see existing alerts'),
        )
        verbose_name_plural = _('analyses')

    def __str__(self):
        return str(self.alert)

    @property
    def analyst(self):
        """The user assigned to the related Alert."""
        return self.alert.assigned_user


class CommentManager(models.Manager):
    """
    Adds methods to the default model manager.
    """

    def get_queryset(self):
        """
        Overrides the default get_queryset method to select related objects.
        """
        default_queryset = super(CommentManager, self).get_queryset()
        return default_queryset.select_related()


class Comment(models.Model):
    """
    Comments for alert objects.
    """
    alert = models.ForeignKey(
        Alert,
        db_index=True,
        related_name='comments',
        related_query_name='comments'
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_date = models.DateTimeField(auto_now_add=True)
    content = RichTextUploadingField()
    tag_relations = GenericRelation(TagRelation, related_query_name='comments')

    objects = CommentManager()

    class Meta(object):
        """Metadata options."""

        permissions = (
            ('view_alert', 'Can see existing alerts'),
        )
        ordering = ['id']

    def get_all_comments(self):
        """Return all |Comments| associated with the |Alert|."""
        return self.alert.comments.all()

    def get_alert_assignee(self):
        """Return the |AppUser| assigned to the |Alert|."""
        return self.alert.assigned_user

    def get_other_contributors(self):
        """Get a list of |AppUsers| who have submitted related |Comments|."""
        assigned_user = self.get_alert_assignee()
        all_comments = self.get_all_comments()
        users = set([comment.user for comment in all_comments])
        if assigned_user:
            users.add(assigned_user)
        users.discard(self.user)
        return list(users)

    def summary(self):
        """Return a summary of the comment."""
        user = self.user.get_full_name()
        date = self.created_date
        content = self.content
        return '%s commented at %s:\n%s' % (user, date, content)
