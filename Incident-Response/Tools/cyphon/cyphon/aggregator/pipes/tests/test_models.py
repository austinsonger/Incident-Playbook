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
Tests the Pipe class and the related RateLimit and SpecSheet classes.
"""

# standard library
try:
    from unittest.mock import Mock, patch
except ImportError:
    from mock import Mock, patch

# third party
from django.test import TestCase
from django.core.exceptions import ValidationError
from testfixtures import LogCapture

# local
from aggregator.pipes.models import Pipe, PipeSpecSheet
from aggregator.reservoirs.models import Reservoir
import platforms.twitter.handlers as twittermodule
from tests.fixture_manager import get_fixtures


class PipesBaseTestCase(TestCase):
    """
    Base class for testing the Pipe class and the related RateLimit
    and SpecSheet classes.
    """
    fixtures = get_fixtures(['pipes', 'plumbers'])


class PipeManagerTestCase(PipesBaseTestCase):
    """
    Tests the PipeManager class.
    """

    def test_get_by_natural_key(self):
        """
        Tests the get_by_natural_key method when the Pipe exists.
        """
        pipe = Pipe.objects.get_by_natural_key('twitter', 'SearchAPI')
        self.assertEqual(pipe.pk, 1)

    def test_natural_key_exception(self):
        """
        Tests the get_by_natural_key method when the Pipe does not exist.
        """
        with LogCapture() as log_capture:
            natural_key = ['fake_platform', 'SearchAPI']
            msg = 'Pipe for "%s %s" does not exist' % (natural_key[0],
                                                       natural_key[1])
            Pipe.objects.get_by_natural_key(*natural_key)
            log_capture.check(
                ('ambassador.endpoints.models', 'ERROR', msg),
            )


class PipeTestCase(PipesBaseTestCase):
    """
    Tests the Pipe class.
    """

    def test_str(self):
        """
        Tests the string representation of a Pipe.
        """
        twitter_pipe = Pipe.objects.get(pk=2)
        self.assertEqual(str(twitter_pipe), 'Twitter PublicStreamsAPI')

    def test_dup_pipes_are_invalid(self):
        """
        Tests that a Pipe with the same API info as another can't be saved.
        """
        twitter = Reservoir.objects.get(name='twitter')

        with self.assertRaises(ValidationError):
            duplicate = Pipe(platform=twitter,
                             api_module='handlers',
                             api_class='PublicStreamsAPI')
            duplicate.full_clean()

    def test_get_specsheet_when_presnt(self):
        """
        Tests the get_specsheet method for getting the SpecSheet for a Pipe
        when the SpecSheet is defined.
        """
        twitter_pipe = Pipe.objects.get(pk=2)
        twitter_specsheet = PipeSpecSheet.objects.get(pipe=2)
        self.assertEqual(twitter_pipe.get_specsheet(), twitter_specsheet)

    def test_get_specsheet_when_absent(self):
        """
        Tests the get_specsheet method for getting the SpecSheet for a Pipe
        when the SpecSheet is undefined.
        """
        facebook_pipe = Pipe.objects.get(pk=3)
        self.assertEqual(facebook_pipe.get_specsheet(), None)

    def test_get_module(self):
        """
        Tests the _get_module method for getting the module for a Pipe's Reservoir.
        """
        twitter_pipe = Pipe.objects.get(pk=1)
        self.assertEqual(twitter_pipe._get_module(), twittermodule)

    def test_create_request_handler(self):
        """
        Tests the create_request_handler method for getting a query handler for a Pipe.
        """
        twitter_pipe = Pipe.objects.get(pk=1)
        user = Mock()
        task = Mock()
        mock_handler = Mock()
        with patch('platforms.twitter.handlers.SearchAPI',
                   return_value=mock_handler) as mock_api:
            kwargs = {
                'user': user,
                'params': {'task': task}
            }
            result = twitter_pipe.create_request_handler(**kwargs)
            mock_api.assert_called_once_with(endpoint=twitter_pipe, user=user,
                                             task=task)
            self.assertEqual(result, mock_handler)


class SpecSheetTestCase(PipesBaseTestCase):
    """
    Tests the SpecSheet class.
    """

    def test_str(self):
        """
        Tests the string representation of a SpecSheet.
        """
        specsheet = PipeSpecSheet.objects.get(pipe=2)
        self.assertEqual(str(specsheet), 'Twitter PublicStreamsAPI')

