from rest_framework.response import Response
from .serailizers import CompanySerializers
from rest_framework.views import APIView
from .models import Company
from django.http import HttpResponse, JsonResponse
from .models import *
from django.views.generic import View
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from nm_jobs.serializers import PerksSerializer, JobsSerializer
from django.shortcuts import get_object_or_404

class PerksView(View):    
    def get(self, request, *args, **kwargs):
        return HttpResponse("Get response for perks view.")

    def post(self, request, *args, **kwargs):
        # input_data = json.loads(request.body)
        # p = Perks(perk_id=input_data["perk_id"], perks=input_data["perks"])
        # p.save()
        perk_data = JSONParser().parse(request)
        perk_serializer = PerksSerializer(data=perk_data)
        if perk_serializer.is_valid():
            perk_serializer.save()
        return JsonResponse({"Status": "Perk inserted into DB"})
    
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
        companies = Company.objects.all()
        serializer = CompanySerializers(companies, many = True)
        return Response(serializer.data)

    def post(self, request):
        pass