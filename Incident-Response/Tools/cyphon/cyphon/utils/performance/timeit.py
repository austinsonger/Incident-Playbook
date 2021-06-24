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
import time


def timeit(func=None, loops=1, verbose=False):
    """
    based on: https://blog.jyore.com/2013/07/python-timing-decorator/
    """
    if func != None:
        def inner(*args, **kwargs):

            sums = 0.0
            mins = 1.7976931348623157e+308
            maxs = 0.0

            print('\n====%s Timing====' % func.__name__)

            for num in range(0, loops):

                # time function
                start_time = time.time()
                result = func(*args, **kwargs)
                deltatime = time.time() - start_time

                # update stats
                if deltatime < mins:
                    mins = deltatime
                if deltatime > maxs:
                    maxs = deltatime
                sums += deltatime

                if verbose == True:
                    print('\t%s ran in %s sec on run %s'
                          % (func.__name__, deltatime, num))

            print('%s min run time was %s sec' % (func.__name__, mins))
            print('%s max run time was %s sec' % (func.__name__, maxs))
            print('%s avg run time was %s sec in %s runs'
                  % (func.__name__, sums/loops, loops))
            print('==== end ====\n')

            return result

        return inner
    else:
        def partial_inner(func):
            return timeit(func, loops, verbose)
        return partial_inner

