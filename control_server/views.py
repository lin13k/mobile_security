from rest_framework import viewsets
from django.db import transaction
from control_server.models import Device, Event
from control_server.serializers import EventSerializer
from control_server.serializers import DeviceWriteSerializer


# class AlarmViewSet(viewsets.ModelViewSet):
#     queryset = Alarm.objects.all()
#     serializer_class = AlarmSerializer


# class DeviceViewSet(viewsets.ModelViewSet):
#     queryset = Device.objects.all()
#     serializer_class = DeviceSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class DeviceViewSet(viewsets.ModelViewSet):
    lookup_field = 'imei'
    queryset = Device.objects.all()

    @transaction.atomic()
    def get_queryset(self):
        imei = self.kwargs['imei']
        if len(Device.objects.filter(imei=imei)) == 0:
            Device.objects.create(imei=imei)
        return Device.objects.all()

    def get_serializer_class(self):
        return DeviceWriteSerializer

    def update(self, request, imei):
        instance = Device.objects.filter(imei=imei)[0]
        new_events = request.data.pop('events')
        for d in new_events:
            Event.objects.create(
                device=instance,
                latitude=d['latitude'],
                longitude=d['longitude'])
        instance.alarm_type = request.data.get(
            'alarm_type', instance.alarm_type)
        instance.save()
