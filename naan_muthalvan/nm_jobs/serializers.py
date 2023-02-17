from rest_framework import serializers
from nm_jobs.models import Perks

class PerksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perks
        fields = ("perk_id", "perks")