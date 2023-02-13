from django.contrib import admin
from .models import Jobs, JobDetails, AddOns, Perks

# Register your models here.
admin.site.register(Jobs)
admin.site.register(JobDetails)
admin.site.register(AddOns)
admin.site.register(Perks)