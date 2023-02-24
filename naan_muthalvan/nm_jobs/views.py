from django.http import HttpResponse, JsonResponse
from django.http.response import JsonResponse

from .models import *
from nm_jobs.serializers import *

from rest_framework.views import APIView
from rest_framework.parsers import JSONParser 
from rest_framework import status

import json
import datetime
import itertools


def index(request):
    return JsonResponse({"status":"success", "msg":"nm jobs index page loaded successfully."}, status=200)

class PerksView(APIView):    
    def get(self, request, *args, **kwargs):
        perks = Perks.objects.values_list("perk", flat=True)
        perks = list(perks)
        return JsonResponse({"status":"success", "msg":"perk data retrieved", "data":perks})

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
        count = Perks.objects.filter(perk=data["perks"]).delete()
        return JsonResponse({'message': '{} perks were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)
    
    def put(self, request):
        perk_data = JSONParser().parse(request)
        perk_instance = Perks.objects.get(perk_id=perk_data["perk_id"])
        perk_instance.perk = perk_data["perks"]
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
        job_instance.perk = job_data["perks"]
        job_instance.save()
        return JsonResponse({"Status": "Job updated successfully"})

class CompanyView(APIView):    
    def get(self, request, *args, **kwargs):
        company = Company.objects.all()
        company = list(company)
        return JsonResponse({"status":"success", "msg":"company data retrieved", "data":company})    

    def post(self, request, *args, **kwargs):
        try:
            data = JSONParser().parse(request)
            serializer = CompanySerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({"status": "success", "msg":"company inserted successfully", "data": serializer.data}, status=200)
            else:
                return JsonResponse({"status": "failed", "msg": "Company Insert: Invalid Data"}, status=400)
        except Exception as e:
            return JsonResponse({"status": "failed", "msg": e}, status=500)

class SpocView(APIView):    
    def get(self, request, *args, **kwargs):
        spoc = Spoc.objects.values_list("name", "phone_no", "email")
        data = dict()
        data["name"] = spoc[0][0]
        data["phone_no"] = spoc[0][1]
        data["email"] = spoc[0][2]
        # spoc = list(itertools.chain(*spoc))
        return JsonResponse({"status":"success", "msg":"spoc data retrieved", "data":data})    

    def post(self, request, *args, **kwargs):
        try:
            data = JSONParser().parse(request)
            serializer = SpocSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({"status": "success", "msg":"spoc inserted successfully", "data": serializer.data}, status=200)
            else:
                return JsonResponse({"status": "failed", "msg": "Spoc Insert: Invalid Data"}, status=400)
        except Exception as e:
            return JsonResponse({"status": "failed", "msg": e}, status=500)

def PostJob(request):
    data = JSONParser().parse(request)

    job_id = ""

    # fields = ("job_id", "job_type", "title", "description", "category", "link", "number_of_openings",
    #           "work_type", "location", "posted_by", "phone_no", "email")
    job_data = {}
    job_data["job_type"] = data["jobType"]
    job_data["title"] = data["title"]
    job_data["description"] = data["description"]
    job_data["category"] = data["category"]
    job_data["link"] = data["link"]
    job_data["number_of_openings"] = data["numberOfOpenings"]
    job_data["work_type"] = data["workModel"]
    job_data["location"] = data["location"]
    job_data["posted_by"] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    job_data["phone_no"] = data["contactPhone"]
    job_data["email"] = data["contactEmail"]

    try:
        serializer = JobsSerializer(data=job_data)
        if serializer.is_valid():
            job = serializer.save()
            job_id = job.id
        else:
            return JsonResponse({"status": "failed", "msg": "Jobs: Data Error"}, status=400)
    except Exception as e:
        return JsonResponse({"status": "failed", "msg": e}, status=500)

    if data["jobType"] == "Fulltime":
        # fields = ("job_id", "date_range", "currency", "max_salary", "min_salary", "experience")
        fulltime_data = {}
        fulltime_data["job_id"] = job_id
        fulltime_data["date_range"] = data["salaryTerm"]
        fulltime_data["currency"] = data["salaryCurrency"]
        fulltime_data["max_salary"] = data["maxSalary"]
        fulltime_data["min_salary"] = data["minSalary"]
        fulltime_data["experience"] = data["experience"]

        try:
            serializer = JobDetailsSerializer(data=fulltime_data)
            if serializer.is_valid():
                serializer.save()
            else:
                return JsonResponse({"status": "failed", "msg": "Fulltime: Data Error"}, status=400)
        except Exception as e:
            return JsonResponse({"status": "failed", "msg": e}, status=500)
    elif data["jobType"] == "Internship":
        # fields = ("job_id", "stipend", "date_range", "duration", "experience")
        internship_data = {}
        internship_data["job_id"] = job_id
        internship_data["stipend"] = data["stipendType"]
        internship_data["date_range"] = data["salaryTerm"]
        internship_data["duration"] = data["duration"]
        internship_data["currency"] = data["salary"]

        try:
            serializer = InternshipSerializer(data=internship_data)
            if serializer.is_valid():
                serializer.save()
            else:
                return JsonResponse({"status": "failed", "msg": "Internship: Data Error"}, status=400)
        except Exception as e:
            return JsonResponse({"status": "failed", "msg": e}, status=500)
    else:
         return JsonResponse({"status": "failed", "msg": "Invalid Job Type"}, status=400)

    perk_ids = Perks.objects.filter(perk__in=data["otherPerks"]).values_list('id', flat=True)
    for pid in perk_ids:
        addon = AddOns()
        addon.job_id_id=job_id
        addon.perk_id_id=pid
        addon.save()

    return JsonResponse({"status": "success", "msg":"job added successfully", "data":{"job_id":job_id}}, status=200)