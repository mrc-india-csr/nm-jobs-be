from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse

from .models import *
from nm_jobs.serializers import *

from rest_framework.views import APIView
from rest_framework.parsers import JSONParser 
from rest_framework import status
from nm_jobs.serializers import *
from django.core.exceptions import ObjectDoesNotExist

from drf_yasg.utils import swagger_auto_schema

import json
import datetime


def health_response():
    return JsonResponse({"status":"success", "msg":"nm backend is up and running"}, status=200)

def response_value(status, msg, data, code):
    return JsonResponse({"status":status, "msg":msg, "data":data}, status=code)

class PerksView(APIView):    
    def get(self, request, *args, **kwargs):
        perks = Perks.objects.values_list("perk", flat=True)
        perks = list(perks)
        return response_value("success", "retrieved perks data", perks, 200)

    @swagger_auto_schema(request_body=PerksSerializer)
    def post(self, request, *args, **kwargs):
        try:
            data = JSONParser().parse(request)
            serializer = PerksSerializer(data=data)
            if serializer.is_valid():
                print(serializer)
                # serializer.save()
                return response_value("success", "perk inserted", serializer.data, 200)
            else:
                return response_value("failed", serializer.errors, "na", 400)
        except Exception as e:
            return response_value("failed", e, "na", 500)
    
    @swagger_auto_schema(request_body=PerksSerializer)
    def delete(self, request, *args, **kwargs):
        data = json.loads(request.body)
        count = Perks.objects.filter(perk=data["perk"]).delete()
        if count[0] != 0:
            return response_value("success", "perk deleted", count[0], 200)
        else:
            return response_value("success", "no perk with that name: perk not deleted", count[0], 200)
    
    @swagger_auto_schema(request_body=PerksUpdateSerializer)
    def put(self, request):
        data = JSONParser().parse(request)
        try:
            perk_instance = Perks.objects.get(perk=data["perkOld"])
            perk_instance.perk = data["perkNew"]
            perk_instance.save()
            return response_value("success", "perk updated", perk_instance.id, 200)
        except Perks.DoesNotExist:
            return response_value("success", "no perk with that name: perk not updated", "na", 200)

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
                return JsonResponse({"status": "failed", "msg": serializer.errors}, status=400)
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
                return JsonResponse({"status": "failed", "msg": serializer.errors}, status=400)
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
                return JsonResponse({"status": "failed", "msg": "Invalid Json"}, status=400)
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

def post_job(request):
    data = JSONParser().parse(request)
    job_serialized = False
    fulltime_serialized =  False
    internship_serialized = False

    # fields = ("job_id", "job_type", "title", "description", "category", "link", "number_of_openings",
    #           "work_type", "location", "posted_by", "phone_no", "email")
    job_id = "999-temp"
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
        job_serializer = JobsSerializer(data=job_data)
        if job_serializer.is_valid():
            job = job_serializer.save()
            job_id = job.id
            pass
        else:
            return JsonResponse({"status": "failed", "msg": job_serializer.errors}, status=400)
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
            fulltime_serializer = JobDetailsSerializer(data=fulltime_data)
            if fulltime_serializer.is_valid():
                fulltime_serializer.save()
            else:
                return JsonResponse({"status": "failed", "msg": fulltime_serializer.errors}, status=400)
        except Exception as e:
            return JsonResponse({"status": "failed", "msg": e}, status=500)
    elif data["jobType"] == "Internship":
        # fields = ("job_id", "stipend", "date_range","is_pre_placement_offer", "duration", "experience")
        internship_data = {}
        internship_data["job_id"] = job_id
        internship_data["is_pre_placement_offer"] = data["isPPO"]
        internship_data["stipend"] = data["salary"]
        internship_data["currency"] = data["salaryCurrency"]
        internship_data["date_range"] = data["salaryTerm"]
        internship_data["duration"] = data["duration"]

        try:
            intern_serializer = InternshipSerializer(data=internship_data)
            if intern_serializer.is_valid():
                intern_serializer.save()
            else:
                return JsonResponse({"status": "failed", "msg": intern_serializer.errors}, status=400)
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

    return JsonResponse({"status": "success", "msg":"job added successfully", "data":{"job_id":job_id}}, status=201)

class CreateProfile(APIView):
    def data_validator(self, body: dict):
        all_good = True
        message = "success"
        list_of_fields = ["companyName", "companyDescription", "sectors", "country", "city", "contactName", "contactEmail", "contactPhone"]
        # spoc_fields = ["name", "email", "phone_no"]
        for field in list_of_fields:
            if field not in body.keys():
                all_good = False
                message = field+ " is missing"
                break
        if all_good:
            if (type(body["sectors"]) != list):
                all_good = False
                message =  "invalid format for sectors"
        return [all_good, message]
    def delete_company(self, id):
        try:
            company_to_delete = Company.objects.get(id)
            company_to_delete.delete()
            print( "Company " +id+ " deleted")
        except Exception as e:
            print(e)
    def delete_spoc(self, id):
        try:
            spoc_to_delete = Spoc.objects.get(id)
            spoc_to_delete.delete()
            print( "Spoc " +id+ " deleted")
        except Exception as e:
            print(e)

    def post(self, request):
        # tables to interact "company", "sector", "company_sector", "spoc"
        try:
            json_body = JSONParser().parse(request)
            validator = self.data_validator(json_body)
            if validator[0]:
                #Company
                try:
                    company_data = {}
                    company_data["name"] = json_body["companyName"]
                    company_data["description"] = json_body["companyDescription"]
                    company_serializer = CompanySerializer(data=company_data)
                    if company_serializer.is_valid():
                        company_response = company_serializer.save()
                        company_id = company_response.id
                except Exception as e:
                    print(e)
                    return JsonResponse({"status": "failed", "message": "Exception occured while creating job"}, status = 500)

                #SPOC
                try:
                    spoc_data = json_body["spoc"]
                    spoc_data["company_id"] = company_id
                    spoc_serializer = SpocSerializer(data=spoc_data)
                    if spoc_serializer.is_valid():
                        spoc_response = spoc_serializer.save()
                        spoc_id = spoc_response.id
                except Exception as e:
                    print(e)
                    self.delete_company(company_id)
                    return JsonResponse({"status": "failed", "message": "Exception occured while creating Spoc"}, status = 500)
                
                #Company sectors   
                try: 
                    sectors = json_body["sectors"]
                    sector_ids = Sector.objects.filter(department__in=sectors).values_list('id', flat=True)
                    for sid in sector_ids:
                        company_sector = CompanySector()
                        company_sector.company_id = company_id
                        company_sector.sector_id = sid
                        company_sector.save()    
                except Exception as e:
                    print(e)
                    self.delete_spoc(spoc_id)
                    self.delete_company(company_id)
                    return JsonResponse({"status": "failed", "message": "Exception occured while creating company sectors"}, status = 500)

            return JsonResponse({"status": "failed", "message": validator[1]})

        except Exception as e:
            print(e)
            return JsonResponse({"status": "failed", "msg": "internal server error"}, status=500)
        
class StoreImg(APIView):
    def post(self, request):
        data = JSONParser().parse(request)
        img_data = {"name": data["name"]}
        # img_data["image"]= data["binary_data"]
        img_data["image"] = convert_To_Binary("nm_jobs/test.jpg")
        img_serializer = ImgSerializer(data=img_data)
        if img_serializer.is_valid():
            response = img_serializer.save()
            print("Image saved")
        else:
            print(img_serializer.errors)
        return JsonResponse({"status": "success", "img_id": response.id})
    
    def get(self, request):
        binary_img = ImageTest.objects.get(id = "d27ec91c-40ae-4260-b97c-c6661c46b55a")
        serializer = ImgSerializer(binary_img)
        if serializer.data:
            print(serializer.data)
            binary_to_file(serializer.data["image"], "achu.txt")
        return JsonResponse({"msg":"success"})
  
def convert_To_Binary(filename):
    with open(filename, 'rb') as file:
        data = file.read()
    return data

def binary_to_file(BLOB, FileName):
    try:
        with open(f"{FileName}", 'wb') as file:
            file.write(BLOB)
        print("achu.jpg stored")
        return "All done"
    except Exception as e:
        print(e)
        return "Failed"
