import logging
from django.contrib.auth import get_user_model
from rest_framework import serializers
from ais.models import Vessel, Position

User = get_user_model()
logger = logging.getLogger("api")


class VesselSerializer(serializers.ModelSerializer):
    positions = serializers.SerializerMethodField("_get_positions")
    last_known = serializers.SerializerMethodField("_last_known_position")
    num_positions = serializers.SerializerMethodField("_num_positions")
    class Meta:
        model = Vessel
        fields = ("id", "mmsi", "num_positions", "positions", "last_known", "dist_covered",)

    def _num_positions(self, obj):
        return obj.num_positions

    def _get_positions(self, obj):
        return obj.positions_list

    def _last_known_position(self, obj):
        return obj.last_known_location
