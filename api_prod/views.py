# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import HumanoidApi
from .serializers import HumanoidApiSerializer

import clmh
import os
# Create your views here.

@csrf_exempt
def snippet_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        humanoid = HumanoidApi.objects.all()
        serializer = HumanoidApiSerializer(humanoid, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = HumanoidApiSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            clmh.saviour(serializer.data['age'], serializer.data['gender'], serializer.data['weight_kg'], serializer.data['body_fat_distribution'], serializer.data['height_cm'], serializer.data['name'], serializer.data['key_string'], serializer.data['image_path'], serializer.data['chest_cm'], serializer.data['waist_cm'], serializer.data['skin_color'])

            fpa = os.path.abspath(os.curdir) + '/static/api_prod/assets/models/' + serializer.data['name'] + '.obj'

            return JsonResponse({'path': fpa}, status=201, safe=False)

        return JsonResponse(serializer.errors, status=400)

def detail(request, path):
	return render(request, 'api/detail.html', {'path': path})