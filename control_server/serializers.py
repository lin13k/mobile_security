from rest_framework import serializers
from control_server.models import Event, Device


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class DeviceReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'
        read_only_fields = ('imei',)


class DeviceWriteSerializer(serializers.ModelSerializer):
    events = EventSerializer(many=True, allow_empty=True)

    class Meta:
        model = Device
        fields = '__all__'
        read_only_fields = ('imei',)
