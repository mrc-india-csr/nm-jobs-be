from django.contrib import admin
from .models import Jobs, FullTime, AddOns, Perks, Sector, Company, CompanySector, Spoc, Status

# Register your models here.
admin.site.register(Jobs)
admin.site.register(FullTime)
admin.site.register(AddOns)
admin.site.register(Perks)
admin.site.register(Status)
admin.site.register(Sector)
admin.site.register(CompanySector)
admin.site.register(Company)
admin.site.register(Spoc)