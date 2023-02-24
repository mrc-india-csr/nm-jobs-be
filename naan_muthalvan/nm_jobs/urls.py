from django.urls import path
from nm_jobs.views import PerksView, SpocView, CompanyView, index, PostJob

from . import views

urlpatterns = [
    path('', index),
    path('perks/', PerksView.as_view()),
    path('postjob/', PostJob),
    path('spoc/', SpocView.as_view()),
    path('company/', CompanyView.as_view())
]