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
Defines sets of choices for use throughout the project.
"""

# local
from utils.dateutils.dateutils import SECONDS, MINUTES, HOURS, DAYS


#: |Alert| priorities.
ALERT_LEVEL_CHOICES = (
    ('CRITICAL', 'Critical'),
    ('HIGH', 'High'),
    ('MEDIUM', 'Medium'),
    ('LOW', 'Low'),
    ('INFO', 'Info'),
)

#: Workflow outcomes for |Alerts|.
ALERT_OUTCOME_CHOICES = (
    ('false positive', 'false positive'),
    ('duplicate', 'duplicate'),
    ('completed', 'completed'),
    ('N/A', 'N/A'),
)

#: Workflow states for |Alerts|.
ALERT_STATUS_CHOICES = (
    ('NEW', 'New'),
    ('BUSY', 'Busy'),
    ('DONE', 'Done'),
)

#: Values from |FIELD_TYPE_CHOICES| that can be searched as dates.
DATE_FIELDS = ['DateTimeField']

#: Fields from mail objects that can be used in data models.
EMAIL_FIELD_CHOICES = (
    ('Attachment', 'Attachment'),
    ('Attachments', 'Attachments'),
    ('Date', 'Date'),
    ('To', 'To'),
    ('From', 'From'),
    ('Subject', 'Subject'),
    ('Content', 'Content'),
)

#: Field type options for fields in data models.
FIELD_TYPE_CHOICES = (
    ('BooleanField', 'BooleanField'),
    ('CharField', 'CharField'),
    ('ChoiceField', 'ChoiceField'),
    ('DateTimeField', 'DateTimeField'),
    ('EmailField', 'EmailField'),
    ('FileField', 'FileField'),
    ('FloatField', 'FloatField'),
    ('IntegerField', 'IntegerField'),
    ('GenericIPAddressField', 'IPAddressField'),
    ('ListField', 'ListField'),
    ('PointField', 'PointField'),
    ('TextField', 'TextField'),
    ('URLField', 'URLField'),
    ('EmbeddedDocument', 'EmbeddedDocument'),
)

GEOCOORDINATE_CHOICES = (
    ('LNG/LAT', 'Longitude, Latitude'),
    ('LAT/LNG', 'Latitude, Logitude'),
)

#: Values from |FIELD_TYPE_CHOICES| that can be geoqueried.
LOCATION_FIELDS = ['PointField']

#: Formats used by API endpoints for geofilters
LOCATION_FORMAT_CHOICES = (
    ('box', 'Bounding Box'),
    ('radius', 'Radius'),
)

#: Logical operators for combining query terms.
LOGIC_CHOICES = (
    ('AND', 'AND'),
    ('OR', 'OR'),
)

#: Health statuses for |Monitors|.
MONITOR_STATUS_CHOICES = (
    ('RED', 'Red'),
    ('YELLOW', 'Yellow'),
    ('GREEN', 'Green'),
)

#: Operators that can be used in searches to filter field values.
OPERATOR_CHOICES = (
    ('eq', 'equals'),
    ('in', 'contains'),
    ('gt', 'greater than'),
    ('gte', 'greater than or equal to'),
    ('lt', 'less than'),
    ('lte', 'less than or equal to'),
    ('regex', 'contains'),
    ('not:eq', 'does not equal'),
    ('not:in', 'does not contain'),
    ('not:regex', 'does not contain'),
    ('not:missing', 'is not null'),
    ('within', 'within')
)

RANGE_CHOICES = (
    ('FloatField:>', 'greater than'),
    ('FloatField:>=', 'greater than or equal to'),
    ('FloatField:<', 'less than'),
    ('FloatField:<=', 'less than or equal to'),
)

REGEX_CHOICES = (
    ('CharField:x', 'contains'),
    ('CharField:^x', 'begins with'),
    ('CharField:x$', 'ends with'),
    ('CharField:^x$', 'equals'),
)

#: Search task options for Reservoir queries.
SEARCH_TASK_CHOICES = (
    ('ADHOC_SRCH', 'Ad hoc search'),
    ('BKGD_SRCH', 'Background search'),
)

#: Categories for broadly categorizing field types.
TARGET_TYPE_CHOICES = (
    ('Account', 'Account'),
    ('DateTime', 'DateTime'),
    ('IPAddress', 'IPAddress'),
    ('Keyword', 'Keyword'),
    ('Location', 'Location'),
)

#: Values from |FIELD_TYPE_CHOICES| that can be searched as text.
TEXT_FIELDS = [
    'CharField',
    'ChoiceField',
    'EmailField',
    'GenericIPAddressField',
    'ListField',
    'TextField',
    'URLField',
]

#: Time unit options.
TIME_UNIT_CHOICES = (
    (SECONDS, 'Seconds'),
    (MINUTES, 'Minutes'),
    (HOURS, 'Hours'),
    (DAYS, 'Days'),
)

