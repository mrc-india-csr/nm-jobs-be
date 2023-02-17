from django.urls import path
from nm_jobs.views import PerksView, CompanyList, TestModelId

urlpatterns = [
    path('companies/', CompanyList.as_view(), name = "company"),
    path('perks/', PerksView.as_view()),
    path('test/', TestModelId.as_view()),
]