from django.http import JsonResponse
from .jobs import *
from .profile import *

def health_response():
    return JsonResponse({"status":"success", "msg":"nm backend is up and running"}, status=200)