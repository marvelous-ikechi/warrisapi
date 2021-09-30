from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .serializers import FileSerializer
import pandas
from .models import File
import json

# from django.utils import simplejson
from django.http import HttpResponse

class FileView(APIView):

  parser_classes = (MultiPartParser, FormParser)

  def post(self, request, *args, **kwargs):
    file_serializer = FileSerializer(data=request.data)
    
    

    if file_serializer.is_valid():
      file_serializer.save()
      return Response(file_serializer.data, status=status.HTTP_201_CREATED)
    else:
      return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def get(self, request,id, format=None):

    snippets = File.objects.get(id=id)
    excel_data_df = pandas.read_excel(snippets.file_name.path, sheet_name="Sheet1")

    json_str = excel_data_df.to_json()
    # serializer = FileSerializer(json_str, many=True)

    print('Excel Sheet to JSON:\n', json_str)
    # return JsonResponse(json.dumps(json_str))
    return HttpResponse(json.dumps(json_str))
  