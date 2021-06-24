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
Defines models for analyzing data.

===================  ========================================================
Class                Description
===================  ========================================================
:class:`~Protocol`   Analyzes data using a function in a Lab subpackage.
:class:`~Procedure`  Applies a Protocol to one or all fields of a dictionary.
===================  ========================================================

"""

# standard library
import importlib

# third party
from django.db import models

# local
from cyphon.models import GetByNameManager
from lab.registry import LAB_CHOICES
from utils.parserutils import parserutils
from utils.validators.validators import IDENTIFIER_VALIDATOR


class Protocol(models.Model):
    """Analyzes data using a function in a Lab subpackage.

    Attributes
    ----------
    name : str
        The name of the Protocol.

    package : str
        The name of a subpackage within the `labs` package that will
        analyze the data.

    module : str
        The name of the module in the package that will analyze the data.

    function : str
        The name of the function that will analyze the data.

    """

    name = models.CharField(max_length=255, unique=True)
    package = models.CharField(
        max_length=32,
        validators=[IDENTIFIER_VALIDATOR],
        choices=LAB_CHOICES
    )
    module = models.CharField(
        max_length=32,
        validators=[IDENTIFIER_VALIDATOR]
    )
    function = models.CharField(
        max_length=32,
        validators=[IDENTIFIER_VALIDATOR]
    )

    objects = GetByNameManager()

    class Meta(object):
        """Metadata options."""

        unique_together = ('package', 'module', 'function')

    def __str__(self):
        """Represent a Protocol as a string."""
        return self.name

    def _get_module(self):
        """Return the module for analyzing the data."""
        module_full_name = 'lab.%s.%s' % (self.package, self.module)

        # load the module (will raise ImportError if module cannot be loaded)
        module = importlib.import_module(module_full_name)

        return module

    def process(self, data):
        """Analyze a dictionary of data.

        Passes data to the Protocol's :attr:`~Protocol.function` and
        returns the result.

        Parameters
        ----------
        data : dict
            The data to analyze.

        Returns
        -------
        any
            The result of the analysis.

        """
        module = self._get_module()

        # get the classifier function (will raise AttributeError if function cannot be found)
        func = getattr(module, self.function)

        return func(data)


class Procedure(models.Model):
    """Applies a Protocol to one or all fields of a dictionary.

    Attributes
    ----------
    name : str
        The name of the procedure.

    protocol : str
        A Protocol used to analyze the data.

    field_name : str
        The name of the field containing the data to analyze. If none
        is provided, the entire data dictionary is analyzed.

    """

    name = models.CharField(max_length=255, unique=True)
    protocol = models.ForeignKey(Protocol)
    field_name = models.CharField(max_length=255, blank=True, null=True)

    objects = GetByNameManager()

    def __str__(self):
        """Represent a Procedure as a string."""
        return self.name

    def _analyze(self, data):
        return self.protocol.process(data)

    def get_result(self, data):
        """Analayze data according to a Protocol.

        Analyzes a data dictionary using the Procedure's
        :attr:`~Procedure.protocol`. If the Procedure has a
        :attr:`~Procedure.field_name`, only the corresponding field
        within the data dictionary is analyzed. Otherwise, the entire
        data dictionary is analyzed with the protocol.

        Parameters
        ----------
        data : dict
            The data to analyze.

        Returns
        -------
        any
            The results of the analysis.

        Notes
        -----
        This method should have the same name as the corresponding
        method in an Inspection.

        """
        if self.field_name:
            value = parserutils.get_dict_value(self.field_name, data)
            return self._analyze(value)
        else:
            return self._analyze(data)
