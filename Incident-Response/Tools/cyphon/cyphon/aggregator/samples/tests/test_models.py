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
Tests the Taste class.
"""

# third party
from django.test import TestCase
from testfixtures import LogCapture

# local
from aggregator.pipes.models import Pipe
from aggregator.samples.models import Sample
from tests.fixture_manager import get_fixtures


class SampleManagerTestCase(TestCase):
    """
    Tests the SampleManager class.
    """
    fixtures = get_fixtures(['samples'])

    def test_get_by_natural_key(self):
        """
        Tests the get_by_natural_key method when the Sample exists.
        """
        sample = Sample.objects.get_by_natural_key('twitter', 'SearchAPI')
        self.assertEqual(sample.pk, 1)

    def test_natural_key_exception(self):
        """
        Tests the get_by_natural_key method when the Sample does not
        exist.
        """
        with LogCapture() as log_capture:
            Sample.objects.get_by_natural_key('youtube', 'DataAPI')
            log_capture.check(('aggregator.samples.models', 'ERROR',
                               'Sample for Pipe "youtube DataAPI" does not exist'))


class SampleTestCase(TestCase):
    """
    Tests the Sample class.
    """
    fixtures = get_fixtures(['samples'])

    def test_str(self):
        """
        Tests the __str__ method.
        """
        pipe = Pipe.objects.get_by_natural_key('twitter', 'SearchAPI')
        sample = Sample(
            pipe=pipe,
            author='from',
            title='subject',
            content='body',
            location=None,
            datetime='date'
        )
        self.assertEqual(str(sample), 'Twitter SearchAPI')

