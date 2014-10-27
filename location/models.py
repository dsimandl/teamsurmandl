from django.db import models
from django.core.exceptions import ValidationError

from profiles.models import SurmandlUser


class Location(models.Model):
    location_title = models.CharField('Current Location', max_length=255)
    map_center_longitude = models.CharField(max_length=10, null=False)
    map_center_latitude = models.CharField(max_length=10, null=False)
    pin_longitude = models.CharField(max_length=10, null=False)
    pin_latitude = models.CharField(max_length=10, null=False)
    author = models.ForeignKey(SurmandlUser, limit_choices_to={'is_staff': True},
                               related_name='location', verbose_name='Admin User')
    current_location = models.BooleanField(default=False)

    def __unicode__(self):
        return self.location_title

    def clean_fields(self, exclude=None):
        if Location.objects.filter(current_location=True) and self.current_location:
            raise ValidationError("There can be only one current location!")
        else:
            super(Location, self).clean_fields(exclude=None)