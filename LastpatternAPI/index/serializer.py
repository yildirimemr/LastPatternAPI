from rest_framework import serializers
from .models import *


class PredictionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = PredictionModel
        fields = "__all__"
