from django.urls import path
from nm_jobs.views import PerksView, JobsView, post_job

from . import views

urlpatterns = [
    path('', JobsView.as_view()),
    path('perks/', PerksView.as_view()),
    path('postjob/', post_job)
]