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

class PerksView(APIView):    
    def get(self, request):
        perks = Perks.objects.all()
        serializer = PerksSerializer(perks, many = True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
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
    
    def delete(self, request, *args, **kwargs):
        count = Perks.objects.all().delete()
        return JsonResponse({'message': '{} perks were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)

    # def put(self, request):
    #     perk_data = JSONParser().parse(request)
    #     perk_instance = Perks.objects.get(perk_id=perk_data["perk_id"])
    #     perk_instance.perks = perk_data["perks"]
    #     perk_instance.save()
    #     return JsonResponse({"Status": "Perk updated successfully"})

class JobsView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("Get response for jobs view.")

    def post(self, request, *args, **kwargs):
        job_data = JSONParser().parse(request)
        job_serializer = JobsSerializer(data=job_data)
        if job_serializer.is_valid():
            job_serializer.save()
        return JsonResponse({"Status": "Job inserted into DB"})
    
    def delete(self, request, *args, **kwargs):
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
            new_id = uuid.uuid4()
            try:
                body = JSONParser().parse(request)
            except ValueError:
                return JsonResponse({"status": "failed", "msg": "Invalid Json"}, status=400)
            body["company_id"] = str(new_id)
            serializer = CompanySerializer(data=body)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({"status": "success","msg":serializer.data, "id": new_id}, status=200)
            else:
                return JsonResponse({"status": "failed", "msg": serializer.errors}, status=400)
        except Exception as e:
            print(e)
            return JsonResponse({"status": "failed", "msg": "internal server error"}, status=500)

class CompanyWithName(APIView):
    def get(self, request, name):
        try:
            companies = Company.objects.get(name = name)
            serializer = CompanySerializer(companies)
            if serializer.data:
                return Response(serializer.data, status=200)
            else:
                return Response(serializer.errors, status=400)
        except Exception as e:
            return JsonResponse({"status": "failed", "msg": "internal server error"}, status=500)
    
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