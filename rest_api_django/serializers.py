from dataclasses import fields
from rest_framework import serializers
from .models import IoT_Data

class IotdataSerializer(serializers.ModelSerializer):
    class Meta:
        model = IoT_Data
        fields = ['id', 'Serial_no', 'Device_id', 'Device_name']