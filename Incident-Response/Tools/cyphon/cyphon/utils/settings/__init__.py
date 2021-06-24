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

"""

# standard library
import io
import os

# third party
import boto3
import botocore.exceptions
from ec2_metadata import ec2_metadata
import requests


# Determine if the application is running in an AWS EC2 instance.
ON_EC2 = False
if os.path.exists('/sys/hypervisor/uuid'):  # pragma: no cover
    with io.open('/sys/hypervisor/uuid', 'r') as f:
        if f.read().startswith('ec2'):
            try:
                ON_EC2 = bool(ec2_metadata.instance_id)
            except requests.Timeout:
                pass


def get_ssm_param(name, decrypt=True):
    """Fetch a configuration parameter from EC2 Systems Manager (SSM).

    Parameters
    ----------
    name : |str|
        The name of the parameter.

    decrypt : |bool|
        Whether to return a decrypted value for a secure string parameter.

    """
    client = boto3.client('ssm')
    try:
        response = client.get_parameter(Name=name, WithDecryption=decrypt)
        return response['Parameter']['Value']
    except KeyError:
        return None
    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] == 'ParameterNotFound':
            return None
        raise


def get_param(name, default=None, envvar=None, decrypt_ssm=True,
              prefix='cyphon.'):
    """Fetch a configuration parameter from SSM or the environment.

    Parameters
    ----------
    name : |str|
        The name of the parameter.

    default : |str|
        The value to return if the environment variable is undefined.

    envvar : |str|
        The environment variable associated with the parameter.

    prefix : |str| or |None|
        The prefix used for Cyphon parameters in SSM. Default is "cyphon.".

    decrypt_ssm : |bool|
        Whether to return a decrypted value for a secure string parameter.

    """
    if ON_EC2:
        prefix = prefix or ''
        value = get_ssm_param(prefix + name, decrypt_ssm)
        if value is not None:
            return value

    return os.getenv(envvar or name.upper(), default)
