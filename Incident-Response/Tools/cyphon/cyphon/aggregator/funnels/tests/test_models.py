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
Tests the Funnel class and related classes.
"""

# third party
from django.test import TestCase
from testfixtures import LogCapture

# local
from aggregator.pipes.models import Pipe
from aggregator.funnels.models import Funnel
from bottler.bottles.models import Bottle
from sifter.datasifter.datacondensers.models import DataCondenser
from tests.fixture_manager import get_fixtures


class FunnelBaseTestCase(TestCase):
    """
    Base class for testing the Funnel and FunnelManager classes.
    """
    fixtures = get_fixtures(['funnels'])


class FunnelManagerTestCase(FunnelBaseTestCase):
    """
    Tests the FunnelManager class.
    """

    def test_get_by_natural_key(self):
        """
        Tests the get_by_natural_key method when the Funnel exists.
        """
        actual = Funnel.objects.get_by_natural_key(
            bottle_name='post',
            pipe_natural_key=['twitter', 'SearchAPI']
        )
        expected = Funnel.objects.get(pk=1)
        self.assertEqual(actual, expected)

    def test_natural_key_exception(self):
        """
        Tests the get_by_natural_key method when the Funnel does not
        exist.
        """
        with LogCapture() as log_capture:
            bottle_name = 'fake_bottle'
            msg = 'Funnel for Bottle "%s" and Pipe 1 does not exist' % bottle_name
            Funnel.objects.get_by_natural_key(
                bottle_name=bottle_name,
                pipe_natural_key=['twitter', 'SearchAPI']
            )
            log_capture.check(
                ('aggregator.funnels.models', 'ERROR', msg),
            )

    def test_get_condenser(self):
        """
        Tests the get_condenser method.
        """
        actual = Funnel.objects.get_condenser(
            bottle_name='post',
            pipe_natural_key=['twitter', 'SearchAPI']
        )
        expected = DataCondenser.objects.get_by_natural_key('twitter__post')
        self.assertEqual(actual, expected)

    def test_get_bottle(self):
        """
        Tests the get_bottle method.
        """
        pipe_natural_key = ['twitter', 'SearchAPI']
        pipe_id = Pipe.objects.get_id_from_natural_key(pipe_natural_key)
        condenser = DataCondenser.objects.get_by_natural_key('twitter__post')
        actual = Funnel.objects.get_bottle(
            condenser_id=condenser.pk,
            pipe_id=pipe_id
        )
        expected = Bottle.objects.get(name='post')
        self.assertEqual(actual, expected)


class FunnelTestCase(FunnelBaseTestCase):
    """
    Tests the Funnel class.
    """

    def test_str(self):
        """
        Tests the __str__ method.
        """
        funnel = Funnel.objects.get(pk=1)
        actual = str(funnel)
        expected = 'post <- Twitter SearchAPI'
        self.assertEqual(actual, expected)

