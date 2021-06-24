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

# third party
from bson import json_util
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import render_to_response
from django.template import RequestContext
# from rest_framework import status
# from rest_framework.decorators import api_view
# from rest_framework.response import Response

# local
from . import forms
# from . import serializers


def reservoirquery(request):
    """
    View for displaying and handling the form for building a ReservoirQuery.
    """
    form = forms.ReservoirQueryParametersForm(None)

    return render_to_response('reservoirqueries/reservoirquery.html',
                              {'form': form},
                              context_instance=RequestContext(request))


def reservoirquery_search(request):
    """
    View that takes get parameters from a ReservoirQueryParameters form and
    returns the search results.
    """

    form = forms.ReservoirQueryParametersForm(request.GET or None)

    if form.is_valid():
        parameters = form.save(commit=False)

        if not isinstance(request.user, AnonymousUser):
            parameters.created_by = request.user

        results = parameters.execute_ad_hoc_search()
        json_data = json_util.dumps(list(results))
        return render_to_response('query/results.html',
                                  {'data': json_data},
                                  context_instance=RequestContext(request))

    return render_to_response('query/results.html',
                              {'data': json_util.dumps({})},
                              context_instance=RequestContext(request))

# @api_view(['GET'])
# def social_search(request):
#     """
#     API Endpoint for submitting form data that will be used to find
#     relevant information
#     """
#     if request.method == 'GET':
#         serializer = serializers.SocialSerializer(data=request.data)
#         if serializer.is_valid():
#             instance = serializer.save()
#             search_data = instance.execute_ad_hoc_search()
#             return Response(search_data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
