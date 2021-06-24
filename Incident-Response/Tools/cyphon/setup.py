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
import os
try:
    from pip.download import PipSession
    from pip.req import parse_requirements
except ImportError:
    from pip._internal.download import PipSession
    from pip._internal.req import parse_requirements
from setuptools import find_packages, setup

# parse_requirements() returns generator of pip.req.InstallRequirement objects
INSTALL_REQS = parse_requirements(
    'requirements.txt',
    session=PipSession())

# reqs is a list of requirements
# e.g. ['django==1.5.1', 'mezzanine==1.4.6']
REQUIREMENTS = [str(ir.req) for ir in INSTALL_REQS]

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='cyphon',
    version='1.6.3',
    install_requires=REQUIREMENTS,
    packages=find_packages(),
    include_package_data=True,
    license='GNU General Public License v3 (GPLv3)',
    description='Cyphon Engine',
    long_description=README,
    url='https://cyphon.io/',
    author='ControlScan',
    author_email='cyphondev@controlscan.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.11',  # replace "X.Y" as appropriate
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
)
