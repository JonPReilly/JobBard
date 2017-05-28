from django.contrib import admin

from .models import City, State, Location, Country, Region

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

class CountryAdmin(admin.ModelAdmin):
    search_fields = ['name']

    class Meta:
        model = Country

class RegionAdmin(admin.ModelAdmin):
    search_fields = ['name']

    class Meta:
        model = Region

admin.site.register(City, CityAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Region, RegionAdmin)
# Register your models here.
