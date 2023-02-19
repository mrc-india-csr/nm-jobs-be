from rest_framework import serializers
from rest_framework.fields import CharField, EmailField
from nm_jobs.models import Perks, Jobs, Company


class PerksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perks
        fields = ("id", "perks")

class JobsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jobs
        fields = ("id", "job_type", "title", "description", "category", "link", "number_of_openings",
                  "work_type", "location", "posted_by", "phone_no", "email")

class CompanySerializers(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ("name", "description")

