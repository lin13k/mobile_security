from rest_framework import viewsets
from django.conf import settings
from django.db import transaction
from control_server.models import Device, Event
from control_server.serializers import EventSerializer
from control_server.serializers import DeviceWriteSerializer
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404

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
        new_events = request.data.pop('events', [])
        for d in new_events:
            Event.objects.create(
                device=instance,
                latitude=d['latitude'],
                longitude=d['longitude'])
        instance.alarm_type = request.data.get(
            'alarm_type', instance.alarm_type)
        instance.save()

        return Response(self.get_serializer_class()(instance).data)


def device_list(request):
    context = {}
    context['devices'] = Device.objects.all()
    return render(request, 'control_server/device_list.html', context)


def device_detail(request, pk):
    context = {}
    context['device'] = get_object_or_404(Device, pk=pk)
    context['google_map_dir_key'] = settings.GOOGLE_MAPS_DIR_KEY
    return render(request, 'control_server/device_detail.html', context)


