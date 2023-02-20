from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Company, TestModelId
from django.http import HttpResponse, JsonResponse
from .models import *
from django.views.generic import View
from rest_framework.parsers import JSONParser 
from rest_framework import status
from nm_jobs.serializers import PerksSerializer, JobsSerializer, CompanySerializer, TestModelIdSerializer
from django.shortcuts import get_object_or_404
import uuid
import requests
from django.core.exceptions import ObjectDoesNotExist


class PerksView(APIView):    
    def get(self, request):
        perks = Perks.objects.all()
        serializer = PerksSerializer(perks, many = True)
        return Response(serializer.data)

    def post(self, request):
        try:
            try:
                perk_data = JSONParser().parse(request)
            except ValueError:
                return JsonResponse({"status": "failed", "msg": "Invalid Json"}, status=400)
            perk_serializer = PerksSerializer(data=perk_data)
            if perk_serializer.is_valid():
                perk_serializer.save()
                return JsonResponse({"Status": "Success", "data": perk_serializer.data})
            else:
                return JsonResponse({"status": "failed", "msg": perk_serializer.errors}, status=400)
        except Exception as e:
            print(e)
            return JsonResponse({"status": "failed", "msg": e}, status=500)
    
    def delete(self, request):
        count = Perks.objects.all().delete()
        return JsonResponse({'message': '{} perks were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)

    # def put(self, request):
    #     perk_data = JSONParser().parse(request)
    #     perk_instance = Perks.objects.get(perk_id=perk_data["perk_id"])
    #     perk_instance.perks = perk_data["perks"]
    #     perk_instance.save()
    #     return JsonResponse({"Status": "Perk updated successfully"})

class JobsView(View):
    def get(self, request):
        return HttpResponse("Get response for jobs view.")

    def post(self, request):
        job_data = JSONParser().parse(request)
        job_serializer = JobsSerializer(data=job_data)
        if job_serializer.is_valid():
            job_serializer.save()
        return JsonResponse({"Status": "Job inserted into DB"})
    
    def delete(self, request):
        count = Jobs.objects.all().delete()
        return JsonResponse({'message': '{} jobs were deleted successfully!'.format(count[0])})

    def put(self, request):
        job_data = JSONParser().parse(request)
        job_instance = Jobs.objects.get(perk_id=job_data["perk_id"])
        job_instance.perks = job_data["perks"]
        job_instance.save()
        return JsonResponse({"Status": "Job updated successfully"})

class CompanyList(APIView):
    def get(self, request):
        try:
            companies = Company.objects.all()
            serializer = CompanySerializer(companies, many = True)
            if serializer.data:
                return Response(serializer.data, status=200)
            else:
                return Response(serializer.errors, status=400)
        except Exception as e:
            return JsonResponse({"status": "failed", "msg": "internal server error", "reason": e}, status=500)

    def post(self, request):
        try:
            try:
                body = JSONParser().parse(request)
            except ValueError:
                return JsonResponse({"status": "failed", "msg": "Invalid Json"}, status=400)
            serializer = CompanySerializer(data=body)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({"status": "success","msg":serializer.data}, status=200)
            else:
                return JsonResponse({"status": "failed", "msg": serializer.errors}, status=400)
        except Exception as e:
            print(e)
            return JsonResponse({"status": "failed", "msg": "internal server error"}, status=500)

class CompanyWithName(APIView):
    def get(self, request, name):
        try:
            companies = Company.objects.get(name = name)
        except ObjectDoesNotExist:
            return JsonResponse({"status": "failed", "msg": "requested data is not found"}, status=404)
        serializer = CompanySerializer(companies)
        if serializer.data:
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)
    
    def put(self, request, name):
        try:
            company_data = Company.objects.get(name = name)
            try:
                body = JSONParser().parse(request)
            except ValueError:
                return JsonResponse({"status": "failed", "msg": "invalid data provided"}, status=400)
            serializer = CompanySerializer(company_data, body)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({"status": "Success", "data": serializer.data}, status= 200)
            else:
                return JsonResponse({"status": "Failed", "msg": serializer.errors}, status=400)
        except Exception as e:
            return JsonResponse({"status": "failed", "msg": "internal server error"}, status=500)
    
    def delete(self, request, name):
        try:
            company_data = Company.objects.get(name = name)
            company_data.delete()
            return JsonResponse({"status": "Success", "deleted company": name}, status = 200)
        except Exception as e:
            return JsonResponse({"status": "failed", "msg": "internal server error"}, status=500)

class InsertMultiple(APIView):
    def post(self, request):
        try:
            try:
                body = JSONParser().parse(request)
            except ValueError:
                return JsonResponse({"status": "failed", "msg": "Invalid Json"}, status=400)
            company_values = {}
            company_values["name"] = body["company_name"]
            company_values["description"] = body["company_description"]
            perks_data = body["perks"]

            #Company
            company_serializer = CompanySerializer(data=company_values)
            if company_serializer.is_valid():
                company_serializer.save()
                company_response = company_serializer.data
            else:
                return JsonResponse({"status": "failed", "msg": company_serializer.errors}, status=400)
            
            #Perks
            for perk in perks_data: 
                perk_serializer = PerksSerializer(data={"perks": perk})
                if perk_serializer.is_valid():
                    perk_serializer.save()
                else:
                    return JsonResponse({"status": "failed", "msg": perk_serializer.errors}, status=400)
            return JsonResponse({"msg":"success", "company": company_response, "perks": perks_data}, status = 200)
        except ValueError:
            return JsonResponse({"msg":"json error"}, status = 400)


class TestModelId(APIView):
    def post(self, request):
        try:
            body = JSONParser().parse(request)
            serializer = TestModelIdSerializer(data=body)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({"status": "success","data":serializer.data}, status=200)
            else:
                return JsonResponse({"status": "failed", "msg": serializer.errors}, status=400)
        except Exception as e:
            return JsonResponse({"status": "failed", "msg": "internal server error"}, status=500)