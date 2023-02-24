from django.urls import path
from nm_jobs.views import PerksView, CompanyList, SpocView, CompanyWithName, CompanyView, index, PostJob

from . import views

urlpatterns = [
    path('companies', CompanyList.as_view(), name = "company"),
    path('companies/<str:name>', CompanyWithName.as_view(), name = "company with name"),
    path('', index),
    path('perks/', PerksView.as_view()),
    path('postjob/', PostJob),
    path('spoc/', SpocView.as_view()),
    path('company/', CompanyView.as_view())
]