import logging
from rest_framework import status, viewsets, pagination
from rest_framework.authentication import (BasicAuthentication,
                                           TokenAuthentication, SessionAuthentication, )
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissionsOrAnonReadOnly
from rest_framework.response import Response
from .. serializers import VesselSerializer
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from ais.models import Vessel, Position


User = get_user_model()
logger = logging.getLogger('api')


class ApiAuthMixin(object):
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)

class VesselViewSet(ApiAuthMixin, viewsets.ModelViewSet):


    queryset = Vessel.objects.all().order_by('-dist_covered')
    serializer_class = VesselSerializer

    def get_queryset(self):
        mmsi = self.request.GET.get('mmsi')  # Filter order list by mmsi
        if mmsi:
            return Vessel.objects.filter(mmsi=mmsi)
        return Vessel.objects.all().order_by('dist_covered')

    def list(self, request):
        mmsi = request.GET.get('mmsi')  # Filter order list by mmsi
        if mmsi:
            page = self.paginate_queryset(Vessel.objects.filter(mmsi=mmsi))
        else:
            page = self.paginate_queryset(self.queryset)
        if page is not None:
            ctx = {
                'request': request,
            }
            serializer = VesselSerializer(page, many=True, context=ctx)
            return self.get_paginated_response(serializer.data)

    def retrieve(self, request, pk=None):
        vessel = get_object_or_404(self.queryset, pk=pk)
        serializer = VesselSerializer(vessel, context={'request': request})
        return Response(serializer.data)

