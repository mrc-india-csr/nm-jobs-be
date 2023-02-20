from django.http import HttpResponse, JsonResponse
from .models import *
# from .models import Jobs, JobDetails, Perks, AddOns, Company, CompanySector, Sector, Internship, Status, Spoc
from django.views.generic import View
from rest_framework.response import Response
from rest_framework.views import APIView
import json

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
# from nm_jobs.serializers import PerksSerializer, JobsSerializer, JobDetailsSerializer
from nm_jobs.serializers import *
from django.shortcuts import get_object_or_404

def index(request):
    print(request)
    print(request.method)
    print(Jobs.objects.first())
    data = Jobs.objects.first()
    print(data.description)
    return HttpResponse("App is working fine.")

class PerksView(APIView):    
    def get(self, request, *args, **kwargs):
        perks = Perks.objects.all()
        serializer = PerksSerializer(perks, many = True)
        return JsonResponse({"status":"success", "msg":"perk data retrieved", "data":serializer.data})

    def post(self, request, *args, **kwargs):
        try:
            data = JSONParser().parse(request)
            serializer = PerksSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({"status": "success", "msg": serializer.data}, status=200)
            else:
                return JsonResponse({"status": "failed", "msg": "Perk Insert: Invalid Data"}, status=400)
        except Exception as e:
            return JsonResponse({"status": "failed", "msg": e}, status=500)
    
    def delete(self, request, *args, **kwargs):
        data = json.loads(request.body)
        count = Perks.objects.filter(perks=data["perks"]).delete()
        return JsonResponse({'message': '{} perks were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)
    
    def put(self, request):
        perk_data = JSONParser().parse(request)
        perk_instance = Perks.objects.get(perk_id=perk_data["perk_id"])
        perk_instance.perks = perk_data["perks"]
        perk_instance.save()
        return JsonResponse({"Status": "Perk updated successfully"})

class JobsView(APIView):
    def get(self, request, *args, **kwargs):
        return HttpResponse("Get response for jobs view.")

    def post(self, request, *args, **kwargs):
        try:
            data = JSONParser().parse(request)
            serializer = JobsSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({"status": "success", "msg": serializer.data}, status=200)
            else:
                return JsonResponse({"status": "failed", "msg": "Perk Insert: Invalid Data"}, status=400)
        except Exception as e:
            return JsonResponse({"status": "failed", "msg": e}, status=500)
    
    def delete(self, request, *args, **kwargs):
        count = Jobs.objects.all().delete()
        return JsonResponse({'message': '{} jobs were deleted successfully!'.format(count[0])})

    def put(self, request):
        job_data = JSONParser().parse(request)
        job_instance = Jobs.objects.get(perk_id=job_data["perk_id"])
        job_instance.perks = job_data["perks"]
        job_instance.save()
        return JsonResponse({"Status": "Job updated successfully"})
    
def add_job(request):
    data = JSONParser().parse(request)

    job_id = ""
    try:
        serializer = JobsSerializer(data=data)
        if serializer.is_valid():
            job_id = serializer.save()
        else:
            return JsonResponse({"status": "failed", "msg": "Jobs: Data Error"}, status=400)
    except Exception as e:
        return JsonResponse({"status": "failed", "msg": e}, status=500)

    data["job_id"] = job_id.id

    if data["job_type"] == "Fulltime":
        try:
            serializer = FullTimeSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            else:
                return JsonResponse({"status": "failed", "msg": "Fulltime: Data Error"}, status=400)
        except Exception as e:
            return JsonResponse({"status": "failed", "msg": e}, status=500)
    elif data["job_type"] == "Internship":
        try:
            serializer = InternshipSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            else:
                return JsonResponse({"status": "failed", "msg": "Internship: Data Error"}, status=400)
        except Exception as e:
            return JsonResponse({"status": "failed", "msg": e}, status=500)
    else:
        return JsonResponse({"status": "failed", "msg": "Invalid Job Type"}, status=400)  
    
    perk_id = Perks.objects.filter(perks__in=data["perks"]).values_list('id', flat=True)
    for pid in perk_id:
        addon = AddOns()
        addon.job_id_id=job_id.id
        addon.perk_id_id=pid
        addon.save()
    
    return JsonResponse({"Status": "Job added successfully"})