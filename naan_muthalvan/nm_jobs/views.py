from django.http import HttpResponse, JsonResponse
from .models import *
# from .models import Jobs, JobDetails, Perks, AddOns, Company, CompanySector, Sector, Internship, Status, Spoc
from django.views.generic import View
import json

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from nm_jobs.serializers import PerksSerializer
from django.shortcuts import get_object_or_404

def index(request):
    print(request)
    print(request.method)
    print(Jobs.objects.first())
    data = Jobs.objects.first()
    print(data.description)
    return HttpResponse("App is working fine.")

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