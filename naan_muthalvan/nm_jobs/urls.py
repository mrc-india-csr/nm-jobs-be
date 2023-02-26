from django.urls import re_path
from nm_jobs.views import PerksView, CompanyList, SpocView, CompanyWithName, CompanyView, CreateProfile, health_response, post_job

from . import views

urlpatterns = [
    re_path(r'^companies/?$', CompanyList.as_view(), name = "company"),
    re_path(r'^companies/<str:name>/?$', CompanyWithName.as_view(), name = "company with name"),
    re_path(r'^health/?$', health_response),
    re_path(r'^perks/?$', PerksView.as_view()),
    re_path(r'^postjob/?$', post_job),
    re_path(r'^spoc/?$', SpocView.as_view()),
    re_path(r'^company/?$', CompanyView.as_view()),
    re_path(r'^profile/?$', CreateProfile.as_view()),
]