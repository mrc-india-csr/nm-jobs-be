from rest_framework import serializers
from rest_framework.fields import CharField, EmailField
from nm_jobs.models import Perks, Jobs, Company, TestModelId

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ("id","name", "description")
# from nm_jobs.models import Perks, Jobs
from nm_jobs.models import *

class JobsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jobs
        # fields = ("job_id", "job_type", "title", "description", "category", "link", "number_of_openings",
        #           "work_type", "location", "posted_by", "phone_no", "email")
        fields = ("__all__")

class JobDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobDetails
        # fields = ("job_id", "date_range", "currency", "max_salary", "min_salary", "experience")
        fields = ("__all__")

class InternshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Internship
        # fields = ("job_id", "stipend", "date_range", "duration", "experience")
        fields = ("__all__")

class AddOnsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddOns
        # fields = ("job_id", "perk_id")
        fields = ("__all__")

class PerksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perks
        fields = ("__all__",)
