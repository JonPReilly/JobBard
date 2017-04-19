from django.contrib import admin

from .models import City, State, Location

class CityAdmin(admin.ModelAdmin):
    search_fields = ['name']
    class Meta:
        model = City

class StateAdmin(admin.ModelAdmin):
    search_fields = ['name']
    class Meta:
        model = State

class LocationAdmin(admin.ModelAdmin):
    search_fields = ['city__name','state__name',]
    class Meta:
        model = Location

admin.site.register(City, CityAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(Location, LocationAdmin)
# Register your models here.
