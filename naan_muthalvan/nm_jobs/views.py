import json, uuid, datetime, logging
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser 
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import OperationalError
from drf_yasg.utils import swagger_auto_schema
from .models import *
from nm_jobs.serializers import *
from nm_jobs.serializers import *
from django.db import connection

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO, datefmt='%d-%b-%y %H:%M:%S')
logger = logging.getLogger("Naan_Muthalvan_logger")

def health_response():
    return JsonResponse({"status":"success", "msg":"nm backend is up and running"}, status=200)

def response_value(status, msg, data, code):
    return JsonResponse({"status":status, "msg":msg, "data":data}, status=code)

class SectorView(APIView):
    def post(self, request):
        try:
            data = JSONParser().parse(request)
            sector_serializer = SectorSerializer(data=data)
            if sector_serializer.is_valid():
                sector_serializer.save()
                return response_value("success", "sector inserted", sector_serializer.data, 200)
            else:
                return response_value("failed", sector_serializer.errors, "NA", 400)
        except Exception as e:
            return response_value("failed", e.__class__.__name__, "na", 500)

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
                serializer.save()
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
        # jobs = Jobs.objects.values_list("job_type", "title", "description", "category", "link", "number_of_openings",
        #       "work_type", "location", "posted_by", "phone_no", "email")
        # jobs = list(jobs)

        # jobs = JobDetails.objects.select_related().all()
        # for i in jobs:
        #     print(i.job_id.job_type)
        # print(jobs)
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
            # res = cursor.fetchall()
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
            # res = cursor.fetchall()
            intern_jobs = dictfetchall(cursor)

            result = fulltime_jobs + intern_jobs
            return response_value("success", "jobs retrieved", result, 200)

        return JsonResponse({"status":"success", "msg":"jobs retrieved", "data":"na"})

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
        company = Company.objects.values_list("name", flat=True)
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
        if len(spoc) > 0:
            data = dict()
            data["name"] = spoc[0][0]
            data["phone_no"] = spoc[0][1]
            data["email"] = spoc[0][2]
            # spoc = list(itertools.chain(*spoc))
            return response_value("success", "spoc data retrieved", data, 200)   
        else:
            return response_value("failed", "no spoc registered", "na", 200) 

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
            logger.error(e)
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

    job_id = ""

    # insert job details
    try:
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
        # job_data["posted_by"] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        job_data["posted_by"] = data["contactName"]
        job_data["phone_no"] = data["contactPhone"]
        job_data["email"] = data["contactEmail"]

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
        file_data = {}
        file_data["job_id"] = job_id
        byte_array = data["descFile"]
        file_data["file_name"] = data["title"]
        file_data["upload_file"] = bytes(byte_array)
        file_serializer = FilesSerializer(data=file_data)
        if file_serializer.is_valid():
            file_serializer.save()
        else:
            Jobs.objects.filter(id=job_id).delete()
            return response_value("failed", file_serializer.errors, "na", 400)

    # insert fulltime or internship details
    if data["jobType"] == "Fulltime":
        try:
            # fields = ("job_id", "date_range", "currency", "max_salary", "min_salary", "experience")
            fulltime_data = {}
            fulltime_data["job_id"] = job_id
            fulltime_data["date_range"] = data["salaryTerm"]
            fulltime_data["currency"] = data["salaryCurrency"]
            fulltime_data["max_salary"] = data["maxSalary"]
            fulltime_data["min_salary"] = data["minSalary"]
            fulltime_data["experience"] = data["experience"]

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
            # fields = ("job_id", "stipend", "date_range","is_pre_placement_offer", "duration", "currency")
            internship_data = {}
            internship_data["job_id"] = job_id
            internship_data["is_pre_placement_offer"] = data["isPPO"]
            internship_data["stipend"] = data["salary"]
            internship_data["currency"] = data["salaryCurrency"]
            internship_data["date_range"] = data["salaryTerm"]
            internship_data["duration"] = data["duration"]

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
        # fields = ("job_id", "date_posted", "to_date", "status", "application_received", "company_id")
        status_data = {}
        status_data["job_id"] = job_id
        status_data["date_posted"] = datetime.datetime.now()
        # status_data["to_date"] = datetime.datetime.strptime(data["toDate"], "%d/%m/%Y %H:%M:%S")
        status_data["to_date"] = datetime.datetime.strptime(data["openUntil"], "%d/%m/%Y")
        status_data["status"] = "Open"
        status_data["application_received"] = 0
        status_data["company_id"] = data["companyId"]

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
        # addon = AddOns()
        # addon.job_id_id=job_id
        # addon.perk_id_id=pid
        # addon.save()

    return response_value("success", "job addded successfully", {"job_id":job_id}, "201")

class ProfileView(APIView):
    def get(self, request, company_name):
        try:
            company_get_query = """
                SELECT c.id, c.name, c.description, c.city, c.country, s.name, s.phone_no, s.email, cs.sector_id_id
                FROM nm_jobs_company AS c
                INNER JOIN nm_jobs_spoc AS s ON c.id = s.company_id_id
                INNER JOIN nm_jobs_companysector AS cs ON c.id = cs.company_id_id
                WHERE c.name = "%s"
            """ %(company_name)

            cursor = connection.cursor()
            try:
                cursor.execute(company_get_query)
                company_data = cursor.fetchone()
            except OperationalError:
                return response_value("Failed", "Something wrong with given company name", "NA", 400)
            if company_data==None:
                return response_value("Failed", "Company not found", "NA", 404)
            sector_data = Sector.objects.get(id=company_data[8])
            profile_data  = CompanyDetails.objects.get(company_id = company_data[0])
            profile_byte_arr = list(profile_data.image)
            company_obj = {
                "companyID": company_data[0],
                "companyName": company_data[1],
                "companyDescription": company_data[2],
                "city": company_data[3],
                "country": company_data[4],
                "contactName": company_data[5],
                "contactPhone": company_data[6],
                "contactEmail": company_data[7],
                "sector": sector_data.industry,
                "profileImage": profile_byte_arr,
            }
            return JsonResponse({"data": company_obj})
        except Exception as e:
            return response_value("Failed", "Unexpected error"+ e.__class__.__name__,"NA", 500)

    def data_validator(self, body: dict):
        all_good = True
        message = "success"
        list_of_fields = ["companyName", "companyDescription", "sector", "country", "city", "contactName", "contactEmail", "contactPhone", "profileImage"]
        for field in list_of_fields:
            if field not in body.keys():
                all_good = False
                message = field+ " is missing"
                break
        return [all_good, message]
    
    def delete_company(self, company_id):
        try:
            company_to_delete = Company.objects.get(id=company_id)
            company_to_delete.delete()
        except ObjectDoesNotExist:
            logger.error("company with "+str(company_id) + " doesn't exist")
        logger.info( "Company " +str(company_id)+ " deleted")

    def post(self, request):
        # tables to interact "company", "sector", "company_sector", "spoc"
        try:
            json_body = JSONParser().parse(request)
            validator = self.data_validator(json_body)
            if validator[0]:
                company_id = uuid.uuid4()
                #Company
                try:
                    company_data = {"id": company_id, "name": json_body["companyName"], "description": json_body["companyDescription"]}
                    company_serializer = CompanySerializer(data=company_data)
                    if company_serializer.is_valid():
                        company_serializer.save()
                    else:
                        return JsonResponse({"status": "failed", "message": company_serializer.errors}, status = 400)
                except Exception as e:
                    logger.error(e)
                    return JsonResponse({"status": "failed", "message": "Exception occured while creating company", "error": e.__class__.__name__}, status = 500)

                #SPOC
                try:
                    spoc_data = {
                        "name": json_body["contactName"],
                        "email": json_body["contactEmail"], 
                        "phone_no": json_body["contactPhone"],
                        "company_id": company_id
                    }
                    spoc_serializer = SpocSerializer(data=spoc_data)
                    if spoc_serializer.is_valid():
                        spoc_serializer.save()
                    else:
                        self.delete_company(company_id)
                        return JsonResponse({"status": "failed", "message": spoc_serializer.errors}, status = 400)
                except Exception as e:
                    logger.error(e)
                    self.delete_company(company_id)
                    return JsonResponse({"status": "failed", "message": "Exception occured while creating Spoc", "error": e.__class__.__name__}, status = 500)
            
                #Company details(image)
                try:
                    if json_body["profileImage"]!="null":
                        company_details = {"company_id": company_id, "file_name": json_body["companyName"], "image": bytes(json_body["profileImage"])}
                        image_serializer = CompanyDetailsSerializer(data=company_details)
                        if image_serializer.is_valid():
                            image_serializer.save()
                        else:
                            self.delete_company(company_id)
                            return JsonResponse({"status": "failed", "message": image_serializer.errors}, status = 400)
                except Exception as e:
                    logger.error(e)
                    self.delete_company(company_id)
                    return JsonResponse({"status": "failed", "message": "Exception occured while inserting profile image", "error": e.__class__.__name__}, status = 500)
                
                #Company sectors   
                try: 
                    sector_name = json_body["sector"]
                    try:
                        sector_data = Sector.objects.get(industry= sector_name)
                    except ObjectDoesNotExist:
                        self.delete_company(company_id)
                        return JsonResponse({"status": "failed", "message": "sector '"+sector_name + "' does not exist"}, status = 400)
                    sector_id = sector_data.id
                    company_id_for_sector = company_id
                    company_sector = {"company_id": company_id_for_sector, "sector_id": sector_id}
                    company_sector_serializer = CompanySectorSerializer(data=company_sector)
                    if company_sector_serializer.is_valid():
                        company_sector_serializer.save()
                    else:
                        self.delete_company(company_id)
                        return JsonResponse({"status": "failed", "message": company_sector_serializer.errors}, status = 400)
                except Exception as e:
                    logger.error(e)
                    self.delete_company(company_id)
                    return JsonResponse({"status": "failed", "message": "Exception occured while creating company sectors", "error": e.__class__.__name__}, status = 500)
            
                return JsonResponse({"status": "success", "message": {"company_id" : company_id}})
            else:
                return JsonResponse({"status": "failed", "msg": validator[1]}, status=422)
                
        except Exception as e:
            logger.error(e)
            return JsonResponse({"status": "failed", "msg": "internal server error", "error": e.__class__.__name__}, status=500)

class JobFilesView(APIView):
    def get(self, request):
        files = Files.objects.values_list("file_name", "upload_file")
        files = list(files)
        response_data = {}
        for file in files:
            response_data[file[0]] = list(file[1])
        return response_value("success", "retrieved job files", response_data, 200)

class CompanyImageView(APIView):
    def get(self, request):
        files = CompanyDetails.objects.values_list("file_name", "image")
        files = list(files)
        response_data = {}
        for file in files:
            response_data[file[0]] = list(file[1])
        return response_value("success", "retrieved company images", response_data, 200)
 
class StoreImg(APIView):
    def post(self, request):
        data = JSONParser().parse(request)
        img_data = {"name": data["name"]}
        # img_data["image"]= data["binary_data"]
        img_data["image"] = convert_To_Binary("nm_jobs/test.jpg")
        img_serializer = ImgSerializer(data=img_data)
        if img_serializer.is_valid():
            response = img_serializer.save()
            logger.info("Image saved")
        else:
            logger.error(img_serializer.errors)
        return JsonResponse({"status": "success", "img_id": response.id})
    
    def get(self, request):
        binary_img = ImageTest.objects.get(id = "b0214849b8ab4a529f78d7a29f599026")
        serializer = ImgSerializer(binary_img)
        if serializer.data:
            return JsonResponse({"msg":"success","byte_array": list(serializer.data["image"])})
  
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
