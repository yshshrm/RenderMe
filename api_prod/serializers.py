from rest_framework import serializers
from django.db import models
from .models import HumanoidApi

class HumanoidApiSerializer(serializers.ModelSerializer):

    class Meta:
        model = HumanoidApi
        fields = ('name', 'key_string', 'image_path', 'gender', 'age', 'skin_color','height_cm', 'weight_kg', 'chest_cm', 'waist_cm',  'body_fat_distribution')