from rest_framework import serializers
# from nm_jobs.models import Perks, Jobs
from nm_jobs.models import *

class JobsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jobs
        # fields = ("job_id", "job_type", "title", "description", "category", "link", "number_of_openings",
        #           "work_type", "location", "posted_by", "phone_no", "email")
        fields = ("__all__")

class FullTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FullTime
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
        # fields = ("id", "perk")
        fields = ("__all__")