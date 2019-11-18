import logging
from pprint import pformat
from django.conf import settings
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers
from ais.models import Vessel, Position
User = get_user_model()
logger = logging.getLogger('api')

class VesselSerializer(serializers.ModelSerializer):
    positions = serializers.SerializerMethodField('_get_positions')


    class Meta:
        model = Vessel
        fields = (
            'mmsi',
            'positions',
        )

    def _get_positions(self, obj):
        return obj.positions_list
