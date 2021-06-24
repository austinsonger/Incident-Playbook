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
Tests the Reservoir class, the Reservoir Manager, and the related Gateway class.
"""

# third party
from django.test import TestCase
from django.core.exceptions import ValidationError

# local
from aggregator.reservoirs.models import Reservoir, Gateway
from tests.fixture_manager import get_fixtures


class ReservoirModelsTestCase(TestCase):
    """
    Base class for testing Reservoir class and related classes.
    """
    fixtures = get_fixtures(['reservoirs', 'gateways'])


class ReservoirTestCase(ReservoirModelsTestCase):
    """
    Tests the Reservoir class.
    """

    def setUp(self):
        self.twitter = Reservoir.objects.get(name='twitter')
        self.facebook = Reservoir.objects.get(name='facebook')

    def test_limit_choices_to_registry(self):
        """
        Tests whether social media platform names are limited to
        those listed in the reservoir registry.
        """
        with self.assertRaises(ValidationError):
            unregistered = Reservoir(name='unregistered platform',
                                     enabled=True)
            unregistered.full_clean()

    def test_get_gateway(self):
        """
        Tests method for getting a gateway for a given task.
        """
        twitter_gateway = Gateway.objects.get(reservoir=self.twitter,
                                              task='ADHOC_SRCH')
        self.assertEqual(self.twitter.get_gateway('ADHOC_SRCH'), twitter_gateway)
        self.assertEqual(self.twitter.get_gateway('BOGUS'), None)

    def test_get_pipe(self):
        """
        Tests method for getting a pipe for a given task.
        """
        twitter_gateway = Gateway.objects.get(reservoir=self.twitter,
                                              task='ADHOC_SRCH')
        self.assertEqual(self.twitter.get_pipe('ADHOC_SRCH'), twitter_gateway.pipe)

        # test a gateway without the specified pipe
        self.assertEqual(self.twitter.get_pipe('BOGUS'), None)

        # test a gateway with no pipe
        youtube = Reservoir.objects.get(name='youtube')
        self.assertEqual(youtube.get_pipe('ADHOC_SRCH'), None)


class ReservoirManagerTestCase(ReservoirModelsTestCase):
    """
    Tests the ReservoirManager class.
    """

    def test_find_enabled(self):
        """
        Tests method for finding enabled platforms.
        """
        platforms = Reservoir.objects.find_enabled()
        self.assertEqual(len(platforms), 2)
        self.assertEqual(len(platforms.filter(enabled=True)), len(platforms))

    def test_find_pipes(self):
        """
        Tests method for finding pipes of enabled platforms for
        a given gateway task.
        """
        search_pipes = Reservoir.objects.find_pipes('ADHOC_SRCH')
        self.assertEqual(len(search_pipes), 1)

        stream_pipes = Reservoir.objects.find_pipes('BKGD_SRCH')
        self.assertEqual(len(stream_pipes), 1)

        no_pipes = Reservoir.objects.find_pipes('BOGUS')
        self.assertEqual(len(no_pipes), 0)
