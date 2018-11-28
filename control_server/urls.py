from django.conf.urls import url
from control_server.views import DeviceViewSet, EventViewSet, device_list
from control_server.views import device_detail

event_list = EventViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

event_detail = EventViewSet.as_view({
    'get': 'retrieve',
    'delete': 'destroy',
})


device_views = DeviceViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
})

urlpatterns = [
    url(r'^events/$', event_list, name='event_list'),
    url(r'^event/(?P<pk>[0-9]+)/$', event_detail, name='event_detail'),
    url(r'^sync/(?P<imei>[0-9]+)/$', device_views, name='device_views'),
    url(r'^devices/?$', device_list, name='device_list'),
    url(r'^devices/(?P<pk>[0-9]+)/?$', device_detail, name='device_detail'),
]
