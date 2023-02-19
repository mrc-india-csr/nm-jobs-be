from rest_framework import serializers
from rest_framework.fields import CharField, EmailField
from nm_jobs.models import Perks, Jobs, Company, TestModelId

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ("id","name", "description")

class JobsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jobs
        fields = ("job_id", "job_type", "title", "description", "category", "link", "number_of_openings",
                  "work_type", "location", "posted_by", "phone_no", "email")

class PerksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perks
        fields = ("perks",)

class TestModelIdSerializer(serializers.ModelSerializer):
    name = CharField(required = True)
    class Meta:
        model = TestModelId
        fields = ('id','name','email')