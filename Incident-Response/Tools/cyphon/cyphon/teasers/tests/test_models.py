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
Tests the Teaser class.
"""

# standard library
import datetime
from unittest.mock import Mock, patch

# third party
from django.test import TestCase

# local
from codebooks.models import CodeBook
from django.contrib.gis.geos import Point
from teasers.models import Teaser
from tests.fixture_manager import get_fixtures


class TeaserTestCase(TestCase):
    """
    Tests the Teaser class.
    """

    fixtures = get_fixtures(['codebooks'])

    now = datetime.datetime.now()
    point = Point(-148.000, 32.000)

    def setUp(self):
        self.data = {
            '_raw_data': {
                'backend': 'elasticsearch',
                'database': 'test_index',
                'collection': 'acme'
            },
            'info': {
                'date': self.now,
                'from': 'John Smith',
                'subject': 'Acme & Acme',
                'body': 12345678910123,
                'location': self.point,
            },
        }
        self.mock_teaser_settings = {
            'CHAR_LIMIT': 10
        }
        self.mock_codebooks_settings = {
            'CODENAME_PREFIX': '*',
            'CODENAME_SUFFIX': '*',
        }
        self.mock_distilleries_settings = {
            'RAW_DATA_KEY': '_raw_data',
            'BACKEND_KEY': 'backend',
            'WAREHOUSE_KEY': 'database',
            'COLLECTION_KEY': 'collection',
        }
        with patch.dict('teasers.models.settings.TEASERS',
                        self.mock_teaser_settings):
            with patch.dict('codebooks.models.settings.CODEBOOKS',
                            self.mock_codebooks_settings):
                self.teaser = Teaser(
                    author='info.from',
                    title='info.subject',
                    content='info.body',
                    location='info.location',
                    datetime='info.date',
                )
        # supply a primary key to allow testing of an abstract model
        self.teaser._meta.pk = Mock()
        self.teaser._meta.pk.attname = 'title'

    def test_to_dict(self):
        """
        Tests the _to_dict method.
        """
        actual = self.teaser._to_dict()

        expected = {
            'author': 'info.from',
            'title': 'info.subject',
            'content': 'info.body',
            'location': 'info.location',
            'location_format': 'LNG/LAT',
            'datetime': 'info.date',
            'date_string': None,
            'date_format': None,
        }
        self.assertEqual(actual, expected)

    def test_get_sample_with_datetime(self):
        """
        Tests the get_sample method for a teaser that uses a datetime
        field.
        """
        with patch('teasers.models._TEASER_SETTINGS',
                   self.mock_teaser_settings):
            actual = self.teaser.get_sample(self.data)
            location = actual.pop('location')
            expected = {
                'collection': 'elasticsearch.test_index.acme',
                'author': 'John Smith',
                'title': 'Acme & Acm',
                'content': 12345678910123,
                'date': self.now,
            }
            self.assertEqual(actual, expected)
            self.assertEqual(location.coords, (-148.000, 32.000))

    def test_get_sample_with_date_str(self):
        """
        Tests the get_sample method for a teaser that uses a date string
        field.
        """
        self.teaser.datetime = None
        self.teaser.date_string = 'info.date'
        self.teaser.date_format = '%Y-%m-%d'

        self.data['info']['date'] = '1988-08-16'
        with patch('teasers.models.settings.TEASERS',
                   self.mock_teaser_settings):
            actual = self.teaser.get_sample(self.data)
            date = actual['date']
            self.assertEqual(date.year, 1988)
            self.assertEqual(date.month, 8)
            self.assertEqual(date.day, 16)

    def test_get_blind_sample(self):
        """
        Tests the get_sample method.
        """
        codebook = CodeBook.objects.get_by_natural_key('Acme')
        with patch.dict('teasers.models.settings.TEASERS',
                        self.mock_teaser_settings):
            with patch.dict('codebooks.models.settings.CODEBOOKS',
                            self.mock_codebooks_settings):
                actual = self.teaser.get_blind_sample(self.data, codebook)
                location = actual.pop('location')
                expected = {
                    'collection': 'elasticsearch.test_index.acme',
                    'author': '*FORGE*',
                    'title': '*PEAK* & *',
                    'content': 12345678910123,
                    'date': self.now,
                }
                self.assertEqual(actual, expected)
                self.assertEqual(location.coords, (-148.000, 32.000))

    def test_get_text_fields(self):
        """
        Tests the get_text_fields method.
        """
        actual = self.teaser.get_text_fields()
        expected = ['info.body', 'info.from', 'info.subject']
        self.assertEqual(actual, expected)

