from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Company, TestModelId
from django.http import HttpResponse, JsonResponse
from .models import *
from django.views.generic import View
from rest_framework.parsers import JSONParser 
from rest_framework import status
from nm_jobs.serializers import PerksSerializer, JobsSerializer, CompanySerializers, TestModelIdSerializer
from django.shortcuts import get_object_or_404
import uuid

class PerksView(APIView):    
    def get(self, request):
        perks = Perks.objects.all()
        serializer = PerksSerializer(perks, many = True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        # input_data = json.loads(request.body)
        # p = Perks(perk_id=input_data["perk_id"], perks=input_data["perks"])
        # p.save()
        perk_data = JSONParser().parse(request)
        perk_data["perk_id"] = uuid.uuid4()
        perk_serializer = PerksSerializer(data=perk_data)
        if perk_serializer.is_valid():
            perk_serializer.save()
        return JsonResponse({"Status": "Success", "data": perk_serializer.data})
    
    def delete(self, request, *args, **kwargs):
        count = Perks.objects.all().delete()
        return JsonResponse({'message': '{} perks were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)

    def put(self, request):
        perk_data = JSONParser().parse(request)
        perk_instance = Perks.objects.get(perk_id=perk_data["perk_id"])
        perk_instance.perks = perk_data["perks"]
        perk_instance.save()
        return JsonResponse({"Status": "Perk updated successfully"})

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
            serializer = CompanySerializers(companies, many = True)
            return Response(serializer.data,status=200)
        except Exception as e:
            return JsonResponse({"status": "failed", "msg": "internal server error"}, status=500)

    def post(self, request):
        try:
            print(request)
            new_id = uuid.uuid4()
            body = JSONParser().parse(request)
            body["company_id"] = str(new_id)
            print(body)
            serializer = CompanySerializers(data=body)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({"status": "success","msg":serializer.data, "id": new_id}, status=200)
            else:
                return JsonResponse({"status": "failed", "msg": serializer.errors}, status=400)
        except Exception as e:
            print(e)
            return JsonResponse({"status": "failed", "msg": "internal server error"}, status=500)

    def put(self, request):
        try:
            # company_data = Company.objects.get(company_id = id)
            body = JSONParser().parse(request)
            serializer = CompanySerializers(data=body)
            if serializer.is_valid():
                data = serializer.save()
                return JsonResponse({"status": "success","msg":"Company updated into DB", "id": data.id}, status=200)
            else:
                return JsonResponse({"status": "failed", "msg": serializer.errors}, status=400)
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