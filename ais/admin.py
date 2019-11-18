# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Vessel, Position


class PositionInline(admin.TabularInline):
    model = Position
    extra = 0


@admin.register(Vessel)
class VesselAdmin(admin.ModelAdmin):
    list_display = ('id', 'mmsi', 'num_positions', 'total_positions', 'dist_covered',)
    inlines = (PositionInline,)


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('id', 'vessel', 'lat', 'lon', 'sort',)
