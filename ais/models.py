from django.db import models
from django.utils import timezone


class Vessel(models.Model):

    mmsi = models.IntegerField(
        "MMSI", help_text="Identifier for this vessel", unique=True
    )
    @property
    def num_positions(self):
        return self.position_set.count()

    def __str__(self):
        return "Vessel {}".format(self.mmsi)


class Position(models.Model):
    vessel = models.ForeignKey(Vessel, on_delete=models.CASCADE)
    lat = models.FloatField(
        "latitude",
    )
    lon = models.FloatField(
        "longitude",
    )
    sort = models.IntegerField(
        "Sort", default=0
    )
    def __str__(self):
        return "Vessel Position {} {}".format(self.lat, self.lon)
    #dt = models.DateTimeField(default=timezone.now)
