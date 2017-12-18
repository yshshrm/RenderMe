from rest_framework import serializers

from .models import Humanoid

class HumanoidSerializer(serializers.ModelSerializer):

    class Meta:
        model = Humanoid
        fields =('human_name', 'age', 'muscle', 'gender', 'weight', 'height')