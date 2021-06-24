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
from bottler.containers.models import Container
from bottler.tastes.models import Taste
from tests.fixture_manager import get_fixtures


class TasteManagerTestCase(TestCase):
    """
    Tests the TasteManager class.
    """
    fixtures = get_fixtures(['tastes'])

    def test_get_by_natural_key(self):
        """
        Tests the get_by_natural_key method when the Taste exists.
        """
        taste = Taste.objects.get_by_natural_key('mail')
        self.assertEqual(taste.pk, 3)

    def test_natural_key_exception(self):
        """
        Tests the get_by_natural_key method when the Taste does not exist.
        """
        with LogCapture() as log_capture:
            Taste.objects.get_by_natural_key('post')
            log_capture.check(('bottler.tastes.models', 'ERROR',
                               'Taste for Container "post" does not exist'))


class TasteTestCase(TestCase):
    """
    Tests the Taste class.
    """
    fixtures = get_fixtures(['codebooks', 'tastes'])

    def test_str(self):
        """
        Tests the __str__ method.
        """
        container = Container.objects.get_by_natural_key('mail')
        taste = Taste(
            container=container,
            datetime='date',
            author='from',
            title='subject',
            content='body',
            location=None
        )
        self.assertEqual(str(taste), 'mail')

