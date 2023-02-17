from django.urls import path

from . import views

urlpatterns = [
    path('companies/', views.CompanyList.as_view(), name = "company"),
]