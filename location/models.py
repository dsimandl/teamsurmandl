from django.db import models

from profiles.models import SurmandlUser

class Location(models.Model):
    map_center_longitude = models.CharField(max_length=10, null=False)
    map_center_latitude = models.CharField(max_length=10, null=False)
    pin_longitude = models.CharField(max_length=10, null=False)
    pin_latitude = models.CharField(max_length=10, null=False)
    author = models.ForeignKey(SurmandlUser, limit_choices_to={'is_staff':True},
                               related_name='location', verbose_name='')
    current_location = models.BooleanField(default=False)