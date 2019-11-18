from django.core.management.base import BaseCommand, CommandError
from ais.models import Vessel, Position
import csv
from geopy.distance import geodesic
import logging


class Command(BaseCommand):
    """
    CSV must be in this format: <EntityValue.pk>,<EntityValue.entity>,<EntityValue.name>,mod|item,<pos_id>
    """
    help = ("Import mappings between entity_values => menu pos_ids from a csv in the root project directory.  "
            "Run with ./manage.py import_menu_mapping something.csv 3")

    def add_arguments(self, parser):
        parser.add_argument('filepath', nargs='+', type=str)

    def handle(self, *args, **options):

        try:
            local_file = open(options['filepath'][0], 'r')
        except Exception as e:
            raise CommandError(e)
        created = 0

        reader = csv.reader(local_file)
        count = 0
        test = []
        for r in reader:
            if count == 0:
                count += 1
                continue
            mmsi = int(r[3])
            try:
                lon = float(r[9])
                lat = float(r[10])
                sort = int(r[0])
                print("mmsi: {}, lat: {}, lon: {}".format(mmsi, lat, lon))
            except Exception as e:
                continue
            vessel, created = Vessel.objects.get_or_create(mmsi=mmsi)
            if lat > 90: # means position not available
                continue
            pos, created = Position.objects.get_or_create(vessel=vessel, lat=lat, lon=lon, sort=sort)

            count += 1

        for vessel in Vessel.objects.all():

            traversed = 0
            plist = vessel.positions_list
            for i in range(1, len(plist)):
                p1 = (plist[i - 1].get('lat'), plist[i - 1].get('lon'))
                p2 = (plist[i].get('lat'), plist[i].get('lon'))
                try:
                    traversed += geodesic(p1, p2).meters
                except:
                    print(vessel.id)
            Vessel.objects.filter(pk=vessel.id).update(
                dist_covered = traversed,
                total_positions=Position.objects.values('id').filter(vessel=vessel).count())


