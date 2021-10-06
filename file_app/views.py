from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .serializers import FileSerializer
import pandas
from .models import File
from rest_framework import viewsets
import json
import itertools
import openpyxl

# from django.utils import simplejson
from django.http import HttpResponse


class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all
    serializer_class = FileSerializer


class FileView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file_serializer = FileSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, function, format=None, *args, **kwargs):
        print(args, kwargs, "I was here")
        snippets = File.objects.get(id=kwargs['file_id'])
        excel_data_df = pandas.read_excel(snippets.file_name.path, sheet_name="Sheet1")

        workbook = openpyxl.load_workbook(snippets.file_name.path)
        source = workbook['Sheet1']
        print(source['D1'].value)
        json_str = excel_data_df.to_json()
        # serializer = FileSerializer(json_str, many=True)

        if function == 'multiply':
            product = excel_data_df["Quantity"] * excel_data_df["Unit Price ($)"]
            columns = ['D']
            items_list = iter(product)
            row = 2
            print(items_list)
            for i in range(len(product)):
                for col in columns:
                    source[f"{col}{row}"].value = product[i]
                    row = row + 1
                print(product[i])
                workbook.save(snippets.file_name.path)

        if function == 'sum':
            sum_value = excel_data_df["Quantity"] + excel_data_df["Unit Price ($)"]
            columns = ['D']
            items_list = iter(sum_value)
            row = 2
            print(items_list)
            for i in range(len(sum_value)):
                for col in columns:
                    source[f"{col}{row}"].value = sum_value[i]
                    row = row + 1
                workbook.save(snippets.file_name.path)

        print('Excel Sheet to JSON:\n', json_str)
        # return JsonResponse(json.dumps(json_str))
        return HttpResponse(json.dumps(json_str))


