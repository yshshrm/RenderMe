from rest_framework import serializers
from django.db import models
from .models import HumanoidApi

class HumanoidApiSerializer(serializers.ModelSerializer):

    class Meta:
        model = HumanoidApi
        fields = ('name', 'height_cm', 'weight_kg', 'chest_cm', 'waist_cm', 'age', 'body_fat_distribution')