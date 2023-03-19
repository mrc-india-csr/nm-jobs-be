import json, uuid, datetime, logging
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser 
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import OperationalError
from drf_yasg.utils import swagger_auto_schema
from ..models import *
from nm_jobs.serializers import *
from nm_jobs.serializers import *
from django.db import connection

def response_value(status, msg, data, code):
    return JsonResponse({"status":status, "msg":msg, "data":data}, status=code)

class JobsView(APIView):
    def get(self, request, *args, **kwargs):
        def dictfetchall(cursor): 
            "Returns all rows from a cursor as a dict" 
            desc = cursor.description 
            return [
                    dict(zip([col[0] for col in desc], row)) 
                    for row in cursor.fetchall() 
                    ]
        
        with connection.cursor() as cursor:
            fulltime_query = """
                select 
                    job.title,
                    job.job_type,
                    jd.experience,
                    job.category,
                    job.location,
                    stat.application_received,
                    cast(stat.date_posted as varchar) as date_posted,
                    cast(stat.to_date as varchar) as to_date,
                    job.posted_by
                from nm_jobs_jobs as job
                inner join nm_jobs_jobdetails as jd on job.id = jd.job_id_id
                inner join nm_jobs_status as stat on job.id = stat.job_id_id
            """
            cursor.execute(fulltime_query)
            fulltime_jobs = dictfetchall(cursor)

            intern_query = """
                select 
                    job.title,
                    job.job_type,
                    job.category,
                    job.location,
                    stat.application_received,
                    cast(stat.date_posted as varchar) as date_posted,
                    cast(stat.to_date as varchar) as to_date,
                    job.posted_by
                from nm_jobs_jobs as job
                inner join nm_jobs_internship as int on job.id = int.job_id_id
                inner join nm_jobs_status as stat on job.id = stat.job_id_id
            """
            cursor.execute(intern_query)
            intern_jobs = dictfetchall(cursor)

            result = fulltime_jobs + intern_jobs
            return response_value("success", "jobs retrieved", result, 200)

    def delete(self, request, *args, **kwargs):
        job_data = JSONParser().parse(request)
        job_id = job_data["job_id"]
        
        Internship.objects.filter(job_id=job_id).delete()
        JobDetails.objects.filter(job_id=job_id).delete()
        Files.objects.filter(job_id=job_id).delete()
        Status.objects.filter(id=job_id).delete()
        Perks.objects.filter(id=job_id).delete()
        Jobs.objects.filter(id=job_id).delete()

        return response_value("success", "jobs deleted", "na", 200)

    def put(self, request, *args, **kwargs):
        pass

class PerksView(APIView):    
    def get(self, request, *args, **kwargs):
        perks = Perks.objects.values_list("perk", flat=True)
        perks = list(perks)
        return response_value("success", "retrieved perks data", perks, 200)

    def post(self, request, *args, **kwargs):
        try:
            data = JSONParser().parse(request)
            serializer = PerksSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return response_value("success", "perk inserted", serializer.data, 200)
            else:
                return response_value("failed", serializer.errors, "na", 400)
        except Exception as e:
            return response_value("failed", e, "na", 500)
    
    def delete(self, request, *args, **kwargs):
        data = json.loads(request.body)
        count = Perks.objects.filter(perk=data["perk"]).delete()
        if count[0] != 0:
            return response_value("success", "perk deleted", count[0], 200)
        else:
            return response_value("success", "no perk with that name: perk not deleted", "na", 200)
    
    def put(self, request):
        data = JSONParser().parse(request)
        try:
            perk_instance = Perks.objects.get(perk=data["perkOld"])
            perk_instance.perk = data["perkNew"]
            perk_instance.save()
            return response_value("success", "perk updated", perk_instance.id, 200)
        except Perks.DoesNotExist:
            return response_value("success", "no perk with that name: perk not updated", "na", 200)

def post_job(request):
    data = JSONParser().parse(request)

    job_id = ""

    # insert job details
    try:
        job_data = {
            "job_type" : data["jobType"],
            "title" : data["title"],
            "description" : data["description"],
            "category" : data["category"],
            "link" : data["link"],
            "number_of_openings" : data["numberOfOpenings"],
            "work_type" : data["workModel"],
            "location" : data["location"],
            "posted_by" : data["contactName"],
            "phone_no" : data["contactPhone"],
            "email" : data["contactEmail"]
        }

        job_serializer = JobsSerializer(data=job_data)
        if job_serializer.is_valid():
            job = job_serializer.save()
            job_id = job.id
        else:
            return response_value("failed", job_serializer.errors, "na", 400)
    except Exception as e:
        return response_value("failed", e, "na", 500)

    # insert job description file
    if data["descFile"] != "null":

        byte_array = data["descFile"]
        
        file_data = {
            "job_id" : job_id,
            "file_name" : data["title"],
            "upload_file" : bytes(byte_array)
        }
        
        file_serializer = FilesSerializer(data=file_data)
        if file_serializer.is_valid():
            file_serializer.save()
        else:
            Jobs.objects.filter(id=job_id).delete()
            return response_value("failed", file_serializer.errors, "na", 400)

    # insert fulltime or internship details
    if data["jobType"] == "Fulltime":
        try:
            fulltime_data = {
                "job_id" : job_id,
                "date_range" : data["salaryTerm"],
                "currency" : data["salaryCurrency"],
                "max_salary" : data["maxSalary"],
                "min_salary" : data["minSalary"],
                "experience" : data["experience"]
            }

            fulltime_serializer = JobDetailsSerializer(data=fulltime_data)
            if fulltime_serializer.is_valid():
                fulltime_serializer.save()
            else:
                Files.objects.filter(job_id=job_id).delete()
                Jobs.objects.filter(id=job_id).delete()
                return response_value("failed", fulltime_serializer.errors, "na", 400)
        except Exception as e:
            return response_value("failed", e, "na", 500)
    elif data["jobType"] == "Internship":
        try:
            internship_data = {
                "job_id" : job_id,
                "is_pre_placement_offer" : data["isPPO"],
                "stipend" : data["salary"],
                "currency" : data["salaryCurrency"],
                "date_range" : data["salaryTerm"],
                "duration" : data["duration"]
            }

            intern_serializer = InternshipSerializer(data=internship_data)
            if intern_serializer.is_valid():
                intern_serializer.save()
            else:
                Files.objects.filter(job_id=job_id).delete()
                Jobs.objects.filter(id=job_id).delete()
                return response_value("failed", intern_serializer.errors, "na", 400)
        except Exception as e:
            return response_value("failed", e, "na", 500)
    else:
         return response_value("failed", "invalid job type", "na", 400)
    
    # insert job status
    try:
        status_data = {
            "job_id" : job_id,
            "date_posted" : datetime.datetime.now(),
            "to_date" : datetime.datetime.strptime(data["openUntil"], "%d/%m/%Y"),
            "status" : "Open",
            "application_received" : 0,
            "company_id" : data["companyId"]
        }

        status_serializer = StatusSerializer(data=status_data)
        if status_serializer.is_valid():
            status_serializer.save()
        else:
            Internship.objects.filter(job_id=job_id).delete()
            JobDetails.objects.filter(job_id=job_id).delete()
            Files.objects.filter(job_id=job_id).delete()
            Jobs.objects.filter(id=job_id).delete()

            return response_value("failed", status_serializer.errors, "na", 400)
    except Exception as e:
        return response_value("failed", e, "na", 500)

    # insert perk details
    perk_ids = Perks.objects.filter(perk__in=data["otherPerks"]).values_list('id', flat=True)
    for pid in perk_ids:
        addon_data = {
            "job_id":job_id,
            "perk_id":pid
        }
        addon_serializer = AddOnsSerializer(data=addon_data)
        if addon_serializer.is_valid():
            addon_serializer.save()

    return response_value("success", "job addded successfully", {"job_id":job_id}, "201")
