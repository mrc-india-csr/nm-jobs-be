from django.urls import path
from nm_jobs.views import PerksView, CompanyList, JobsView, CompanyWithName, post_job

from . import views

urlpatterns = [
    path('companies', CompanyList.as_view(), name = "company"),
    path('companies/<str:name>', CompanyWithName.as_view(), name = "company with name"),
    path('', JobsView.as_view()),
    path('perks/', PerksView.as_view()),
    path('postjob/', post_job)
]