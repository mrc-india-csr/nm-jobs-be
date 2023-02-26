from rest_framework import serializers

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
        # fields = ("id", "perk")
        fields = ("__all__")

class SpocSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spoc
        # fields = ("company_id", "name", "phone_no", "email")
        fields = ("__all__")

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        # fields = ("name", "description")
        fields = ("__all__")

class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        # fields = ("industry", "department")
        fields = ("__all__")

class CompanySectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanySector
        # fields = ("sector_id", "company_id")
        fields = ("__all__")
