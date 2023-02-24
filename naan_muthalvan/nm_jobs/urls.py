from django.urls import path
from nm_jobs.views import PerksView, JobsView, PostJob, index

from . import views

urlpatterns = [
    path('', index),
    path('perks/', PerksView.as_view()),
    path('postjob/', PostJob)
]