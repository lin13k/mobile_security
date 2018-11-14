from django.db import models
from geopy import units, distance
from geopy.geocoders.googlev3 import GeocoderQueryError
from geopy import geocoders
from django.conf import settings

# Create your models here.


class GeoManager(models.Manager):
    def near(self, latitude=None, longitude=None, distance_range=30):
        queryset = super(GeoManager, self).get_queryset()

        if not (latitude and longitude and distance_range):
            return queryset.none()

        latitude = float(latitude)
        longitude = float(longitude)
        distance_range = float(distance_range)

        rough_distance = units.degrees(
            arcminutes=units.nautical(kilometers=distance_range)) * 2

        queryset = queryset.filter(
            latitude__range=(
                latitude - rough_distance,
                latitude + rough_distance
            ),
            longitude__range=(
                longitude - rough_distance,
                longitude + rough_distance
            )
        )

        locations = []
        for location in queryset:
            if location.latitude and location.longitude:
                exact_distance = distance.distance(
                    (latitude, longitude),
                    (location.latitude, location.longitude)
                ).kilometers

                if exact_distance <= distance_range:
                    locations.append(location)

        queryset = queryset.filter(id__in=[l.id for l in locations])
        return queryset


class BaseGeo(models.Model):
    address = models.TextField(blank=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    place = models.TextField(blank=True)
    objects = GeoManager()

    class Meta:
        abstract = True

    def save(self, domain='maps.google.com.my', *args, **kwargs):
        address = self.address
        if address:
            if not self.latitude or not self.longitude:
                try:
                    g = geocoders.GoogleV3(
                        api_key=settings.GOOGLE_API_KEY)
                    self.place, (self.latitude,
                                 self.longitude) = g.geocode(address)
                except GeocoderQueryError:
                    print(GeocoderQueryError.args)
                except Exception as e:
                    print('%s' % e)

        super(BaseGeo, self).save(*args, **kwargs)


class Device(models.Model):
    imei = models.TextField(blank=False, unique=True)
    ALARM_TYPE_CHOICES = (
        ('BL', 'Block'),
        ('NT', 'Notification'),
    )
    last_modify_time = models.DateTimeField(auto_now=True)
    alarm_type = models.CharField(
        max_length=2, choices=ALARM_TYPE_CHOICES,
        blank=True)


class Event(BaseGeo):
    create_time = models.DateTimeField(auto_now_add=True)
    device = models.ForeignKey(
        'control_server.Device', on_delete=models.CASCADE,
        related_name='events'
    )



