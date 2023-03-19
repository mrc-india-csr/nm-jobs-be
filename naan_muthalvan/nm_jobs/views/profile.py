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

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO, datefmt='%d-%b-%y %H:%M:%S')
logger = logging.getLogger("Naan_Muthalvan_logger")

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
        if body["profileImage"].__class__.__name__ != 'list':
            all_good = False
            message = "image cannot be other than array"
        for field in list_of_fields:
            if field not in body.keys():
                all_good = False
                message += field+ " is missing"
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
                    company_data = {"id": company_id, 
                                    "name": json_body["companyName"], 
                                    "description": json_body["companyDescription"],
                                    "city": json_body["city"],
                                    "country": json_body["country"]
                                    }
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
            
                return JsonResponse({"status": "success", "message": {"company_id" : company_id}}, status = 201)
            else:
                return JsonResponse({"status": "failed", "msg": validator[1]}, status=422)
                
        except Exception as e:
            logger.error(e)
            return JsonResponse({"status": "failed", "msg": "internal server error", "error": e.__class__.__name__}, status=500)

    def put(self, request, company_id):
        json_body = JSONParser().parse(request)
        # Tables to interact: company, companyDetails, spoc, company sectors
        company_data = Company.objects.get(id = company_id)
        company_image_data = CompanyDetails.objects.get(company_id = company_id)
        spoc_data = Spoc.objects.get(company_id = company_id)
        company_sector_data = CompanySector.objects.get(company_id = company_id)
        
        validator = self.data_validator(json_body)
        if validator[0]:
            #company
            replaced_company_data ={"id": company_id, 
                "name": json_body["companyName"], 
                "description": json_body["companyDescription"],
                "city": json_body["city"],
                "country": json_body["country"]
                }
            company_ser = CompanySerializer(company_data, replaced_company_data)
            #company image
            replaced_company_image_data = {"company_id": company_id, "file_name": json_body["companyName"], "image": bytes(json_body["profileImage"])}
            company_img_ser = CompanyDetailsSerializer(company_image_data, replaced_company_image_data)
            #spoc
            replaced_spoc_data = {
                                "name": json_body["contactName"],
                                "email": json_body["contactEmail"], 
                                "phone_no": json_body["contactPhone"],
                                "company_id": company_id
                            }
            spoc_ser = SpocSerializer(spoc_data, replaced_spoc_data)
            #company sector
            sector_name = json_body["sector"]
            try:
                sector_data = Sector.objects.get(industry= sector_name)
            except ObjectDoesNotExist:
                return JsonResponse({"status": "failed", "message": "sector '"+sector_name + "' does not exist"}, status = 400)
            sector_id = sector_data.id
            replaced_company_sector_data = {"company_id": company_id, "sector_id": sector_id}
            company_sector_ser = CompanySectorSerializer(company_sector_data, replaced_company_sector_data)
            
            if company_ser.is_valid() and company_img_ser.is_valid() and company_sector_ser.is_valid() and spoc_ser.is_valid():
                company_ser.save()
                company_img_ser.save()
                spoc_ser.save()
                company_sector_ser.save()
                return response_value("Success", "profile updated successfully", {"company_id": company_id}, 200)
            
            else:
                value1 = company_ser.is_valid() 
                value2 = company_img_ser.is_valid()
                value3 = company_sector_ser.is_valid()
                value4 = spoc_ser.is_valid()
                return response_value("Failed", {**dict(company_ser.errors), **dict(company_img_ser.errors), **dict(spoc_ser.errors), ** dict(company_sector_ser.errors)}, "NA", 422)

        else:
            return JsonResponse({"status": "failed", "msg": validator[1]}, status=422)

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
