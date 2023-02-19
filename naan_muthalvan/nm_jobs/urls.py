from django.urls import path
from nm_jobs.views import PerksView, CompanyList, JobsView

urlpatterns = [
    path('perks/', PerksView.as_view()),
    path('', JobsView.as_view()),
    path('companies/', CompanyList.as_view(), name = "company"),
]