from ..views.base import (VesselViewSet, )
from django.urls import path, include


urlpatterns = [
    path('vessels/',
         VesselViewSet.as_view({'get': 'list'}),
         name='vessel-list-api'),
    path('orders/<int:pk>/',
         VesselViewSet.as_view({'get': 'retrieve'}),
         name='vessel-detail-api'),
]
