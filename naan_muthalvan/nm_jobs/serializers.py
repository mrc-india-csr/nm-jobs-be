from rest_framework import serializers
from nm_jobs.models import Perks, Jobs, Company

class CompanySerializers(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ("name", "description")

class JobsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jobs
        fields = ("job_id", "job_type", "title", "description", "category", "link", "number_of_openings",
                  "work_type", "location", "posted_by", "phone_no", "email")

class PerksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perks
        fields = (["perks"])