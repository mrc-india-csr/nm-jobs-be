# from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
# from rest_framework.decorators import api_view
from .serailizers import CompanySerializers
# from django.views import View
# from django.shortcuts import render
from rest_framework.views import APIView

from .models import Company

# @api_view(['GET'])
# def company(request):
#     companies = Company.objects.all()
#     serializer = CompanySerializers(companies, many = True)
#     return Response(serializer.data)

class CompanyList(APIView):
    def get(self, request):
        companies = Company.objects.all()
        serializer = CompanySerializers(companies, many = True)
        return Response(serializer.data)

    def post(self, request):
        pass