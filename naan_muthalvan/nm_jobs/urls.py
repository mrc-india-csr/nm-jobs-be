from django.urls import re_path, path
from nm_jobs.views import *

urlpatterns = [
    re_path(r'^companies/?$', CompanyList.as_view(), name = "company"),
    path('companies/<str:name>/', CompanyWithName.as_view(), name = "company with name"),
    re_path(r'^health/?$', health_response),
    re_path(r'^perks/?$', PerksView.as_view()),
    re_path(r'^postjob/?$', post_job),
    re_path(r'^spoc/?$', SpocView.as_view()),
    re_path(r'^company/?$', CompanyView.as_view()),
    re_path(r'^profile/?$', CreateProfile.as_view()),
    re_path(r'^image/?$', StoreImg.as_view()),
    re_path(r'^company_files/?$', FilesView.as_view()),
    re_path(r'^sectors/?$', SectorView.as_view()),
    re_path(r'/?$', JobsView.as_view()),
]