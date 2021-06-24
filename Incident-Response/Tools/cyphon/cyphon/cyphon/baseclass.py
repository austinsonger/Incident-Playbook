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
Defines a BaseClass that can be subclassed to create other base classes.
Provides informative NotImplementedErrors.
"""

# standard library
import inspect


class BaseClass(object):
    """
    A base class that can be subclassed to create other base classes.
    It provides a way to raise informative NotImplementedErrors. This
    allows developers to easily identify the module and class in which
    a method needs to be implemented.

    Classes derived from BaseClass (e.g., |Engine|) are intended
    to be subclassed by other developers to extend the functionality
    of the project.
    """

    def raise_method_not_implemented(self):
        """
        Raises a |NotImplementedError| with a message that specifies
        the module and class in which the error was raised.
        """
        module_name = self.__module__
        class_name = type(self).__name__
        method_name = inspect.stack()[1][3]

        msg = (u'The %s method has not yet been implemented '
               'for the %s.%s class.') % (method_name, module_name, class_name)

        raise NotImplementedError(msg)

    def raise_attr_not_implemented(self, attribute):
        """
        Takes a string representing an attribute that has not been
        been implemented. Raises a |NotImplementedError| with a message
        that specifies the attribute, as well as the module and class in
        which the error was raised.
        """
        module_name = self.__module__
        class_name = type(self).__name__

        msg = (u'%s has not yet been implemented for the %s.%s class.') \
               % (attribute, module_name, class_name)

        raise NotImplementedError(msg)
