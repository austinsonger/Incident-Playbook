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
Tests the settings utility module.
"""

# standard library
import os
try:
    from unittest.mock import MagicMock, patch
except ImportError:
    from mock import MagicMock, patch
from unittest import TestCase

# third party
import botocore.exceptions

# local
import utils.settings


class GetSsmParametersTestCase(TestCase):
    """
    Tests get_ssm_param utility function.
    """

    def setUp(self):
        self.mock_ssm = MagicMock()

    @patch('boto3.client')
    def test_param_exists(self, mock_boto_client):
        """
        Tests the get_ssm_param utility function when the SSM parameter
        is found.
        """
        param = {'Parameter': {'Value': 'bar'}}
        self.mock_ssm.get_parameter.return_value = param
        mock_boto_client.return_value = self.mock_ssm
        self.assertEqual(utils.settings.get_ssm_param('foo'), 'bar')

    @patch('boto3.client')
    def test_key_error(self, mock_boto_client):
        """
        Tests the get_ssm_param utility function when a KeyError is
        raised.
        """
        self.mock_ssm.get_parameter.side_effect = KeyError
        mock_boto_client.return_value = self.mock_ssm
        self.assertEqual(utils.settings.get_ssm_param('foo'), None)

    @patch('boto3.client')
    def test_param_not_found(self, mock_boto_client):
        """
        Tests the get_ssm_param utility function when the SSM parameter
        cannot be found.
        """
        error = botocore.exceptions.ClientError(
            {'Error': {'Code': 'ParameterNotFound'}}, 'GetParameter')
        self.mock_ssm.get_parameter.side_effect = error
        mock_boto_client.return_value = self.mock_ssm
        self.assertEqual(utils.settings.get_ssm_param('foo'), None)

    @patch('boto3.client')
    def test_invalid_action(self, mock_boto_client):
        """
        Tests the get_ssm_param utility function when a InvalidAction
        error occurs.
        """
        error = botocore.exceptions.ClientError(
            {'Error': {'Code': 'InvalidAction'}}, 'GetParameter')
        self.mock_ssm.get_parameter.side_effect = error
        mock_boto_client.return_value = self.mock_ssm
        self.assertRaises(
            botocore.exceptions.ClientError,
            utils.settings.get_ssm_param,
            'foo'
        )


class GetParametersTestCase(TestCase):
    """
    Tests get_param utility function.
    """

    def setUp(self):
        os.environ['FOO1'] = 'bar1'
        os.environ['FOO2'] = 'bar2'
        self.mock_ssm = MagicMock()
        self.client_error = botocore.exceptions.ClientError(
            {'Error': {'Code': 'ParameterNotFound'}}, 'GetParameter')

    @patch('boto3.client')
    def test_get_param(self, mock_boto_client):
        """
        Tests the get_param function.
        """
        utils.settings.ON_EC2 = True
        param = {'Parameter': {'Value': 'bar'}}
        self.mock_ssm.get_parameter.return_value = param
        mock_boto_client.return_value = self.mock_ssm
        with patch('utils.settings.get_ssm_param', return_value='bar') \
                as mock_get_ssm_param:
            actual = utils.settings.get_param('foo')
            expected = 'bar'
            self.assertEqual(actual, expected)
            mock_get_ssm_param.assert_called_with('cyphon.foo', True)

    @staticmethod
    @patch('boto3.client')
    def test_prefix_is_none(mock_boto_client):
        """
        Tests the get_param function when the prefix is None.
        """
        utils.settings.ON_EC2 = True
        with patch('utils.settings.get_ssm_param') as mock_get_ssm_param:
            utils.settings.get_param('foo', prefix=None)
            mock_get_ssm_param.assert_called_with('foo', True)

    @patch('boto3.client')
    def test_ec2_true_wo_default(self, mock_boto_client):
        """
        Tests the get_param function when on EC2, the name does not
        matches an SSM parameter, and no default is not defined.
        """
        utils.settings.ON_EC2 = True
        self.mock_ssm.get_parameter.side_effect = self.client_error
        mock_boto_client.return_value = self.mock_ssm
        actual = utils.settings.get_param('qux')
        expected = None
        self.assertEqual(actual, expected)

    @patch('boto3.client')
    def test_ec2_true_w_default(self, mock_boto_client):
        """
        Tests the get_param function when on EC2, the name does not
        matches an SSM parameter, and no default is defined.
        """
        utils.settings.ON_EC2 = True
        self.mock_ssm.get_parameter.side_effect = self.client_error
        mock_boto_client.return_value = self.mock_ssm
        actual = utils.settings.get_param('qux', default='bar')
        expected = 'bar'
        self.assertEqual(actual, expected)

    @patch('boto3.client')
    def test_ec2_true_w_envvar(self, mock_boto_client):
        """
        Tests the get_param function when on EC2, the name does not
        matches an SSM parameter, but the envvar is defined.
        """
        utils.settings.ON_EC2 = True
        self.mock_ssm.get_parameter.side_effect = self.client_error
        mock_boto_client.return_value = self.mock_ssm
        actual = utils.settings.get_param('qux', envvar='FOO1')
        expected = 'bar1'
        self.assertEqual(actual, expected)

    def test_ec2_false_w_name(self):
        """
        Tests the get_param function when not on EC2 and the name
        matches a defined environment variable.
        """
        utils.settings.ON_EC2 = False
        actual = utils.settings.get_param('foo1')
        expected = 'bar1'
        self.assertEqual(actual, expected)

    def test_ec2_false_w_name_env(self):
        """
        Checks that the envvar is preferred over name when both match
        an environment variable.
        """
        utils.settings.ON_EC2 = False
        actual = utils.settings.get_param('foo1', envvar='FOO2')
        expected = 'bar2'
        self.assertEqual(actual, expected)

    def test_ec2_false_w_default(self):
        """
        Checks that the default value is used if neither the name nor
        the envvar match an environment variable.
        """
        utils.settings.ON_EC2 = False
        actual = utils.settings.get_param('nix', envvar='QUX', default='bar3')
        expected = 'bar3'
        self.assertEqual(actual, expected)

    def test_ec2_false_wo_default(self):
        """
        Tests the get_param function when not on EC2, neither the name
        nor the envvar match a defined environment variable, and no
        default value is provided.
        """
        utils.settings.ON_EC2 = False
        actual = utils.settings.get_param('nix', envvar='QUX')
        expected = None
        self.assertEqual(actual, expected)
