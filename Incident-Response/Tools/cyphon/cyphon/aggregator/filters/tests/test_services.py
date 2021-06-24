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
Tests Filter services.
"""

# standard library
try:
    from unittest.mock import Mock, patch
except ImportError:
    from mock import Mock, patch

# third party
from django.test import TestCase

# local
from aggregator.filters.models import Filter
from aggregator.filters.services import execute_filter_queries
from aggregator.reservoirs.models import Reservoir
from tests.fixture_manager import get_fixtures


class ExecuteFilterQueriesTestCase(TestCase):
    """
    Tests the execute_filter_queries function.
    """
    fixtures = get_fixtures([])

    def test_execute_filter_queries(self):
        """
        Tests the execute_filter_queries function.
        """
        query = 'mock_query'
        stream_task = 'BKGD_SRCH'
        doc_ids = [3, 4, 5]
        mock_results = Mock()
        mock_pumproom = Mock()
        mock_pumproom.get_results = Mock(return_value=mock_results)

        with patch('aggregator.filters.services.PumpRoom',
                   return_value=mock_pumproom) as new_pumproom:
            with patch('aggregator.filters.services.Reservoir.objects'):
                Filter.objects.create_reservoir_query = Mock(return_value=query)
                Reservoir.objects.find_enabled = Mock(return_value=doc_ids)
                results = execute_filter_queries()

                new_pumproom.assert_called_once_with(reservoirs=doc_ids,
                                                     task=stream_task)
                mock_pumproom.get_results.assert_called_once_with(query)
                self.assertEqual(results, mock_results)

