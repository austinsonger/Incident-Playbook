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
Tests AlertAdmin methods.
"""

# standard library
try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock

# third party
from django.contrib import admin
from django.test import TestCase

# local
from alerts.admin import AlertAdmin
from alerts.models import Alert


class AlertAdminTestCase(TestCase):
    """
    Base class for testing the AlertAdmin class.
    """

    def setUp(self):
        self.modeladmin = AlertAdmin(Alert, admin.site)
        self.modeladmin.message_user = Mock()
        self.queryset_single = Mock()
        self.queryset_single.update = Mock(return_value=1)
        self.queryset_multi = Mock()
        self.queryset_multi.update = Mock(return_value=2)
        self.request = Mock()

    def test_set_status_to_new_single(self):
        """
        Tests the set_status_to_new method for one updated alert.
        """
        self.modeladmin.set_status_to_new(self.request, self.queryset_single)
        self.queryset_single.update.assert_called_once_with(status='NEW')
        self.modeladmin.message_user.assert_called_once_with(
            self.request,
            '1 alert was successfully marked as New.')

    def test_set_status_to_new_multi(self):
        """
        Tests the set_status_to_new method for multiple updated alerts.
        """
        self.modeladmin.set_status_to_new(self.request, self.queryset_multi)
        self.queryset_multi.update.assert_called_once_with(status='NEW')
        self.modeladmin.message_user.assert_called_once_with(
            self.request,
            '2 alerts were successfully marked as New.')

    def test_set_status_to_busy_single(self):
        """
        Tests the set_status_to_busy method for one updated alert.
        """
        self.modeladmin.set_status_to_busy(self.request, self.queryset_single)
        self.queryset_single.update.assert_called_once_with(status='BUSY')
        self.modeladmin.message_user.assert_called_once_with(
            self.request,
            '1 alert was successfully marked as Busy.')

    def test_set_status_to_busy_multi(self):
        """
        Tests the set_status_to_busy method for multiple updated alerts.
        """
        self.modeladmin.set_status_to_busy(self.request, self.queryset_multi)
        self.queryset_multi.update.assert_called_once_with(status='BUSY')
        self.modeladmin.message_user.assert_called_once_with(
            self.request,
            '2 alerts were successfully marked as Busy.')

    def test_set_status_to_done_single(self):
        """
        Tests the set_status_to_done method for one updated alert.
        """
        self.modeladmin.set_status_to_done(self.request, self.queryset_single)
        self.queryset_single.update.assert_called_once_with(status='DONE')
        self.modeladmin.message_user.assert_called_once_with(
            self.request,
            '1 alert was successfully marked as Done.')

    def test_set_status_to_done_multi(self):
        """
        Tests the set_status_to_done method for multiple updated alerts.
        """
        self.modeladmin.set_status_to_done(self.request, self.queryset_multi)
        self.queryset_multi.update.assert_called_once_with(status='DONE')
        self.modeladmin.message_user.assert_called_once_with(
            self.request,
            '2 alerts were successfully marked as Done.')

    def test_set_level_to_crit_single(self):
        """
        Tests the set_level_to_critical method for one updated alert.
        """
        self.modeladmin.set_level_to_critical(self.request, self.queryset_single)
        self.queryset_single.update.assert_called_once_with(level='CRITICAL')
        self.modeladmin.message_user.assert_called_once_with(
            self.request,
            '1 alert was successfully marked as critical priority.')

    def test_set_level_to_crit_multi(self):
        """
        Tests the set_level_to_critical method for multiple updated alerts.
        """
        self.modeladmin.set_level_to_critical(self.request, self.queryset_multi)
        self.queryset_multi.update.assert_called_once_with(level='CRITICAL')
        self.modeladmin.message_user.assert_called_once_with(
            self.request,
            '2 alerts were successfully marked as critical priority.')

    def test_set_level_to_high_single(self):
        """
        Tests the set_level_to_high method for one updated alert.
        """
        self.modeladmin.set_level_to_high(self.request, self.queryset_single)
        self.queryset_single.update.assert_called_once_with(level='HIGH')
        self.modeladmin.message_user.assert_called_once_with(
            self.request,
            '1 alert was successfully marked as high priority.')

    def test_set_level_to_high_multi(self):
        """
        Tests the set_level_to_high method for multiple updated alerts.
        """
        self.modeladmin.set_level_to_high(self.request, self.queryset_multi)
        self.queryset_multi.update.assert_called_once_with(level='HIGH')
        self.modeladmin.message_user.assert_called_once_with(
            self.request,
            '2 alerts were successfully marked as high priority.')

    def test_set_level_to_medium_single(self):
        """
        Tests the set_level_to_medium method for one updated alert.
        """
        self.modeladmin.set_level_to_medium(self.request, self.queryset_single)
        self.queryset_single.update.assert_called_once_with(level='MEDIUM')
        self.modeladmin.message_user.assert_called_once_with(
            self.request,
            '1 alert was successfully marked as medium priority.')

    def test_set_level_to_medium_multi(self):
        """
        Tests the set_level_to_medium method for multiple updated alerts.
        """
        self.modeladmin.set_level_to_medium(self.request, self.queryset_multi)
        self.queryset_multi.update.assert_called_once_with(level='MEDIUM')
        self.modeladmin.message_user.assert_called_once_with(
            self.request,
            '2 alerts were successfully marked as medium priority.')

    def test_set_level_to_low_single(self):
        """
        Tests the set_level_to_low method for one updated alert.
        """
        self.modeladmin.set_level_to_low(self.request, self.queryset_single)
        self.queryset_single.update.assert_called_once_with(level='LOW')
        self.modeladmin.message_user.assert_called_once_with(
            self.request,
            '1 alert was successfully marked as low priority.')

    def test_set_level_to_low_multi(self):
        """
        Tests the set_level_to_low method for multiple updated alerts.
        """
        self.modeladmin.set_level_to_low(self.request, self.queryset_multi)
        self.queryset_multi.update.assert_called_once_with(level='LOW')
        self.modeladmin.message_user.assert_called_once_with(
            self.request,
            '2 alerts were successfully marked as low priority.')

    def test_set_outcome_true_single(self):
        """
        Tests the set_outcome_to_true method for one updated alert.
        """
        self.modeladmin.set_outcome_to_true(self.request, self.queryset_single)
        self.queryset_single.update.assert_called_once_with(outcome=True)
        self.modeladmin.message_user.assert_called_once_with(
            self.request,
            '1 alert was successfully marked as True.')

    def test_set_outcome_true_multi(self):
        """
        Tests the set_outcome_to_true method for multiple updated alerts.
        """
        self.modeladmin.set_outcome_to_true(self.request, self.queryset_multi)
        self.queryset_multi.update.assert_called_once_with(outcome=True)
        self.modeladmin.message_user.assert_called_once_with(
            self.request,
            '2 alerts were successfully marked as True.')

    def test_set_outcome_false_single(self):
        """
        Tests the set_outcome_to_false method for one updated alert.
        """
        self.modeladmin.set_outcome_to_false(self.request, self.queryset_single)
        self.queryset_single.update.assert_called_once_with(outcome=False)
        self.modeladmin.message_user.assert_called_once_with(
            self.request,
            '1 alert was successfully marked as False.')

    def test_set_outcome_false_multi(self):
        """
        Tests the set_outcome_to_false method for multiple updated alerts.
        """
        self.modeladmin.set_outcome_to_false(self.request, self.queryset_multi)
        self.queryset_multi.update.assert_called_once_with(outcome=False)
        self.modeladmin.message_user.assert_called_once_with(
            self.request,
            '2 alerts were successfully marked as False.')

