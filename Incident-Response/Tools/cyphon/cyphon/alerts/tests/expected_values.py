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

Expected values for Alert API tests.

"""

ALERT_DETAIL = {
    'id': 4,
    'notes': None,
    'comments': [],
    'created_date': '2015-03-01T02:42:24.468404Z',
    'location': None,
    'assigned_user': None,
    'data': {'content': {'link': 'url', 'text': 'foobar'}},
    'doc_id': '1',
    'incidents': 1,
    'status': 'NEW',
    'link': 'http://localhost:8000/app/alerts/4',
    'dispatches': [],
    'level': 'LOW',
    'tags': [
        {
            'id': 2,
            'name': 'cat',
            'topic': {
                'id': 1,
                'name': 'Animals',
                'url': 'http://testserver/api/v1/topics/1/'
            },
            'article': {
                'id': 2,
                'title': 'Cats',
                'url': 'http://testserver/api/v1/articles/2/'
            }
        }
    ],
    'title': 'Acme Supply Co',
    'url': 'http://testserver/api/v1/alerts/4/',
    'content_date': None,
    'distillery': {
        'id': 1,
        'collection': 1,
        'url': 'http://testserver/api/v1/distilleries/1/',
        'name': 'mongodb.test_database.test_posts',
        'container': {
            'fields': [{
                'field_type': 'CharField',
                'field_name': '_metadata.priority',
                'target_type': 'Keyword'
            }, {
                'field_type': 'PointField',
                'field_name': '_metadata.source_ip_location',
                'target_type': 'Location'
            }, {
                'field_type': 'URLField',
                'field_name': 'content.image',
                'target_type': None
            }, {
                'field_type': 'URLField',
                'field_name': 'content.link',
                'target_type': None
            }, {
                'field_type': 'TextField',
                'field_name': 'content.text',
                'target_type': 'Keyword'
            }, {
                'field_type': 'TextField',
                'field_name': 'content.title',
                'target_type': 'Keyword'
            }, {
                'field_type': 'URLField',
                'field_name': 'content.video',
                'target_type': None
            }, {
                'field_type': 'DateTimeField',
                'field_name': 'created_date',
                'target_type': 'DateTime'
            }, {
                'field_type': 'PointField',
                'field_name': 'location',
                'target_type': 'Location'
            }, {
                'field_type': 'EmailField',
                'field_name': 'user.email',
                'target_type': 'Account'
            }, {
                'field_type': 'CharField',
                'field_name': 'user.id',
                'target_type': None
            }, {
                'field_type': 'URLField',
                'field_name': 'user.link',
                'target_type': None
            }, {
                'field_type': 'CharField',
                'field_name': 'user.name',
                'target_type': 'Account'
            }, {
                'field_type': 'URLField',
                'field_name': 'user.profile_pic',
                'target_type': None
            }, {
                'field_type': 'CharField',
                'field_name': 'user.screen_name',
                'target_type': 'Account'
            }],
            'id': 2,
            'bottle': 3,
            'name': 'labeled_post',
            'taste': {
                'id': 2,
                'date_format': None,
                'location': None,
                'url': 'http://testserver/api/v1/tastes/2/',
                'location_format': 'LNG/LAT',
                'datetime': 'created_date',
                'author': 'user.name',
                'date_string': None,
                'content': 'post.text',
                'title': 'post.title',
                'container': 2
            },
            'url': 'http://testserver/api/v1/containers/2/',
            'label': 1
        },
        'contexts': [{
            'url': 'http://testserver/api/v1/contexts/1/',
            'id': 1,
            'name': 'context_w_filters',
            'filters': [{
                'id': 2,
                'operator': 'eq',
                'url': 'http://testserver/api/v1/contextfilters/2/',
                'value_field': 'content.message',
                'search_field': 'content.subject',
                'operator_text': 'equals',
                'context': 1
            }, {
                'id': 1,
                'operator': 'eq',
                'url': 'http://testserver/api/v1/contextfilters/1/',
                'value_field': 'host',
                'search_field': 'from',
                'operator_text': 'equals',
                'context': 1
            }],
            'before_time_unit': 'm',
            'related_distillery': {
                'id': 3,
                'name': 'elasticsearch.test_index.test_docs',
                'url': 'http://testserver/api/v1/distilleries/3/'
            },
            'primary_distillery': {
                'id': 1,
                'name': 'mongodb.test_database.test_posts',
                'url': 'http://testserver/api/v1/distilleries/1/'
            },
            'filter_logic': 'AND',
            'before_time_interval': 5,
            'after_time_unit': 's',
            'after_time_interval': 10
        }]
    },
    'outcome': None
}

ALERT_LIST = {
    'count': 7,
    'results': [{
        'title': 'No title available',
        'id': 7,
        'url': 'http://testserver/api/v1/alerts/7/',
        'level': 'MEDIUM',
        'created_date': '2015-03-01T02:45:24.468404Z',
        'status': 'DONE',
        'assigned_user': {
            'id': 1,
            'company': None,
            'is_staff': True,
            'first_name': 'John',
            'email': 'testuser1@testdomain.com',
            'last_name': 'Smith'
        },
        'incidents': 1,
        'distillery': None,
        'content_date': None,
        'outcome': None
    }, {
        'title': 'No title available',
        'id': 6,
        'url': 'http://testserver/api/v1/alerts/6/',
        'level': 'HIGH',
        'created_date': '2015-03-01T02:44:24.468404Z',
        'status': 'DONE',
        'assigned_user': {
            'id': 1,
            'company': None,
            'is_staff': True,
            'first_name': 'John',
            'email': 'testuser1@testdomain.com',
            'last_name': 'Smith'
        },
        'incidents': 1,
        'distillery': {
            'id': 2,
            'url': 'http://testserver/api/v1/distilleries/2/',
            'name': 'mongodb.test_database.test_docs'
        },
        'content_date': None,
        'outcome': None
    }, {
        'title': 'No title available',
        'id': 5,
        'url': 'http://testserver/api/v1/alerts/5/',
        'level': 'HIGH',
        'created_date': '2015-03-01T02:43:24.468404Z',
        'status': 'NEW',
        'assigned_user': None,
        'incidents': 1,
        'distillery': {
            'id': 2,
            'url': 'http://testserver/api/v1/distilleries/2/',
            'name': 'mongodb.test_database.test_docs'
        },
        'content_date': None,
        'outcome': None
    }, {
        'title': 'Acme Supply Co',
        'id': 4,
        'url': 'http://testserver/api/v1/alerts/4/',
        'level': 'LOW',
        'created_date': '2015-03-01T02:42:24.468404Z',
        'status': 'NEW',
        'assigned_user': None,
        'incidents': 1,
        'distillery': {
            'id': 1,
            'url': 'http://testserver/api/v1/distilleries/1/',
            'name': 'mongodb.test_database.test_posts'
        },
        'content_date': None,
        'outcome': None
    }, {
        'title': 'Acme Supply Co',
        'id': 3,
        'url': 'http://testserver/api/v1/alerts/3/',
        'level': 'MEDIUM',
        'created_date': '2015-03-01T02:46:24.468404Z',
        'status': 'DONE',
        'assigned_user': {
            'id': 1,
            'company': None,
            'is_staff': True,
            'first_name': 'John',
            'email': 'testuser1@testdomain.com',
            'last_name': 'Smith'
        },
        'incidents': 1,
        'distillery': {
            'id': 1,
            'url': 'http://testserver/api/v1/distilleries/1/',
            'name': 'mongodb.test_database.test_posts'
        },
        'content_date': None,
        'outcome': None
    }, {
        'title': 'Threat Alert',
        'id': 2,
        'url': 'http://testserver/api/v1/alerts/2/',
        'level': 'HIGH',
        'created_date': '2015-03-01T02:41:24.468404Z',
        'status': 'BUSY',
        'assigned_user': None,
        'incidents': 1,
        'distillery': {
            'id': 1,
            'url': 'http://testserver/api/v1/distilleries/1/',
            'name': 'mongodb.test_database.test_posts'
        },
        'content_date': None,
        'outcome': None
    }, {
        'title': 'Acme Supply Co',
        'id': 1,
        'url': 'http://testserver/api/v1/alerts/1/',
        'level': 'HIGH',
        'created_date': '2015-03-01T02:40:24.468404Z',
        'status': 'NEW',
        'assigned_user': None,
        'incidents': 1,
        'distillery': {
            'id': 5,
            'url': 'http://testserver/api/v1/distilleries/5/',
            'name': 'elasticsearch.test_index.test_logs'
        },
        'content_date': None,
        'outcome': None
    }],
    'previous': None,
    'next': None
}
