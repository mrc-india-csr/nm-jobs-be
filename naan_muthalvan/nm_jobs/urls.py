from django.urls import path
from nm_jobs.views import PerksView, JobsView, add_job

from . import views

urlpatterns = [
    path('', JobsView.as_view()),
    path('perks/', PerksView.as_view()),
    path('add_job/', add_job)
]