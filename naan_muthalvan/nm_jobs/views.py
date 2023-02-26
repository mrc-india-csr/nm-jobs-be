from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Company, TestModelId
from django.http import HttpResponse, JsonResponse
from django.http.response import JsonResponse

from .models import *
from nm_jobs.serializers import *

from rest_framework.views import APIView
from rest_framework.parsers import JSONParser 
from rest_framework import status
# from nm_jobs.serializers import PerksSerializer, JobsSerializer, JobDetailsSerializer
from nm_jobs.serializers import *
from django.shortcuts import get_object_or_404
import uuid
import requests
from django.core.exceptions import ObjectDoesNotExist

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
        jobs = Jobs.objects.values_list("job_type", "title", "description", "category", "link", "number_of_openings",
              "work_type", "location", "posted_by", "phone_no", "email")
        jobs = list(jobs)
        return JsonResponse({"status":"success", "msg":"perk data retrieved", "data":jobs})

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
    
    def delete(self, request):
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

def PostJob(request):
    data = JSONParser().parse(request)

    # fields = ("job_id", "job_type", "title", "description", "category", "link", "number_of_openings",
    #           "work_type", "location", "posted_by", "phone_no", "email")
    job_id = ""
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