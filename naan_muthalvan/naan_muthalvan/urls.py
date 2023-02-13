from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('jobs/', include('nm_jobs.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
]
