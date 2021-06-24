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
Creates a signal to send when a |Distillery| saves a document.

========================  ===================================
Constant                  Description
========================  ===================================
:const:`~document_saved`  |Signal| that a document was saved.
========================  ===================================

"""

# third party
from django.db.models.signals import post_save
from django.dispatch import receiver

# local
from distilleries.models import Distillery
from warehouses.models import Collection


@receiver(post_save, sender=Distillery)
@receiver(post_save, sender=Collection)
def put_template(sender, instance, created, **kwargs):
    """Create an index template."""
    try:
        instance.engine.create_template()
    except AttributeError:
        pass
