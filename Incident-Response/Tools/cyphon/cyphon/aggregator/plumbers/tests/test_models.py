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
Tests the Plumber class.
"""

# third party
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from testfixtures import LogCapture

# local
from aggregator.pipes.models import Pipe
from aggregator.plumbers.models import Plumber
from tests.fixture_manager import get_fixtures

USER_MODEL = get_user_model()

TIME = timezone.now()


class PlumberBaseTestCase(TestCase):
    """
    Base class for testing Plumber class and related classes.
    """
    fixtures = get_fixtures(['plumbers'])

    @property
    def plumber(self):
        """
        Retrieves an example Plumber from the database.
        """
        return Plumber.objects.get(pk=1)

    @property
    def pipe(self):
        """
        Retrieves an example Pipe from the database.
        """
        return Pipe.objects.get(pk=1)


class PlumberManagerTestCase(PlumberBaseTestCase):
    """
    Tests the PlumberManager class.
    """

    def test_get_by_natural_key(self):
        """
        Tests get_by_natural_key method for finding a Plumber by name.
        """
        plumber = Plumber.objects.get_by_natural_key('twitter_search')
        self.assertEqual(plumber, self.plumber)

    def test_natural_key_exception(self):
        """
        Tests get_by_natural_key method for when the Plumber does not
        exist.
        """
        with LogCapture() as log_capture:
            plumber_id = 'fake_plumber'
            msg = 'Plumber "%s" does not exist' % plumber_id
            Plumber.objects.get_by_natural_key(plumber_id)
            log_capture.check(
                ('ambassador.emissaries.models', 'ERROR', msg),
            )

    def test_find_public_plumbers(self):
        """
        Tests method for finding plumbers available to all AppUsers.
        """
        plumbers = Plumber.objects.find_public(self.pipe)

        # should retrieve the one public plumber in the test database
        self.assertEqual(len(plumbers), 1)
        self.assertEqual(len(plumbers.filter(passport__public=True)),
                         len(plumbers))

    def test_find_private_plumbers(self):
        """
        Tests method for finding private plumbers for a given AppUser.
        """
        user = USER_MODEL.objects.get(pk=1)
        plumbers = Plumber.objects.find_private(self.pipe, user)
        self.assertEqual(len(plumbers), 2)

        # check that the plumbers are private
        self.assertEqual(
            len(plumbers.filter(passport__public=False)), len(plumbers))

        # check that the plumbers are assigned to the user
        self.assertEqual(
            len(plumbers.filter(endpoints=self.pipe, passport__users=user)),
            len(plumbers)
        )

    def test_find_plumbers_with_pvts(self):
        """
        Tests method for finding plumbers available to a given AppUser,
        when the AppUser has private plumbers.
        """
        user = USER_MODEL.objects.get(pk=1)
        plumbers = Plumber.objects.find_any(self.pipe, user)

        # check that the plumbers are assigned to the user
        self.assertEqual(
            len(plumbers.filter(endpoints=self.pipe, passport__users=user)),
            len(plumbers)
        )

        # check that the correct number are found
        self.assertEqual(len(plumbers), 2)

    def test_find_plumbers_if_no_pvts(self):
        """
        Tests method for finding plumbers available to a given AppUser,
        when the AppUser has no private plumbers.
        """
        user = USER_MODEL.objects.get(pk=3)
        plumbers = Plumber.objects.find_any(self.pipe, user)

        # should find the only public plumber in the test database
        self.assertEqual(len(plumbers), 1)
        self.assertEqual(plumbers[0].pk, 4)


class PlumberTestCase(PlumberBaseTestCase):
    """
    Tests the Plumber class.
    """

    def test_str(self):
        """
        Tests the __str__ method of the Plumber class.
        """
        self.assertEqual(str(self.plumber), 'twitter_search')

