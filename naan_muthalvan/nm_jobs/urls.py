from django.urls import path
from nm_jobs.views import PerksView

from . import views

urlpatterns = [
    path('companies/', views.CompanyList.as_view(), name = "company"),
    path('', views.index, name = "index"),
    path('perks/', PerksView.as_view())
]