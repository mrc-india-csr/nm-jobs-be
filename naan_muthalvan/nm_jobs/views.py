from django.http import HttpResponse, JsonResponse
from .models import Jobs

def index(request):
    print(request)
    print(request.method)
    print(Jobs.objects.first())
    data = Jobs.objects.first()
    print(data.description)
    return JsonResponse({"data": "some data"})