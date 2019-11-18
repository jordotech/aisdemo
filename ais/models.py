from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property

class Vessel(models.Model):
    mmsi = models.IntegerField(
        "MMSI", help_text="Identifier for this vessel", unique=True
    )
    total_positions = models.IntegerField(
        "Positions Recorded", default=0
    )
    dist_covered = models.FloatField("Distance Covered", default=0)
    @property
    def num_positions(self):
        return len(self.positions_list)

    @cached_property
    def positions_list(self):
        ret = []
        for p in Position.objects.filter(vessel=self).order_by('sort'):
            ret.append({
                'lat': p.lat,
                'lng': p.lon,
                'sort': p.sort,
            })
        return ret

    @cached_property
    def last_known_location(self):
        if len(self.positions_list):
            return self.positions_list[0]
        return None
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
    # dt = models.DateTimeField(default=timezone.now)
