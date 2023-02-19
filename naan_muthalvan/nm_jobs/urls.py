from django.urls import path
from nm_jobs.views import PerksView, CompanyList, TestModelId, CompanyWithName

urlpatterns = [
    path('companies', CompanyList.as_view(), name = "company"),
    path('companies/<str:name>', CompanyWithName.as_view(), name = "company with name"),
    path('perks', PerksView.as_view()),
    path('test', TestModelId.as_view()),
]