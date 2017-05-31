from uszipcode import ZipcodeSearchEngine
from location.models import City, State, Location, CitySearchCache, Region, Country
from django.db.models import Q
from pygeocoder import Geocoder, GeocoderError



class LocationManager:
    __search_object = ZipcodeSearchEngine()


    def getCloseLocations(self,location,radius_in_miles =15):
        city_name = location.city.name
        state_name = location.state.name
        try:
            zip_code = self._getZipByCityState(city_name,state_name)
        except ValueError:
            return []
        cities_in_radius = self._getZipCodesNear(zip_code,radius_in_miles)
        return Location.objects.filter(city__pk__in = cities_in_radius )

    def cityQuereyCache(self, location_string):

        try:
            cache_object = CitySearchCache.objects.get(query=location_string)
            print("Cache for " , location_string, cache_object)
            return (True , cache_object.reference)
        except CitySearchCache.DoesNotExist:
            print(location_string, " Not in cache")
            return (False, None)


    def getFromMapsAPI(self, location_string):
        try:
            address = Geocoder.geocode(location_string)
        except GeocoderError:
            return None




        zip = address.postal_code

        if(zip != None):
            try:
                return City.objects.get(zip_code=zip)
            except City.DoesNotExist:

                return None
        formatted_address = address.formatted_address
        if(formatted_address == None):
            return None

        locaiton_array = formatted_address.split(",")
        city_name = locaiton_array[0]
        state = address.state
        if (state == None or city_name == None):
            return None

        possibilities = City.objects.exclude(region=None).filter(name__icontains=city_name, region__name__icontains=state)


        if(possibilities.count() == 0):
            return None

        return possibilities[0]

    def parseCityString(self, location_string):

        loc = location_string.split(",")

        if(len(loc) != 2):
            return self.getFromMapsAPI(location_string)

        city = loc[0]
        region = loc[1]

        possible_cities = City.objects.filter(name__icontains=city).filter(region__code__icontains=region).prefetch_related('region','region__country')


        if(possible_cities.count() > 1):
            return possible_cities[0]
        return self.getFromMapsAPI(location_string)

    def getCity(self, location_string):

        found, cached_object = self.cityQuereyCache(location_string.lower())

        if(found):

            return cached_object

        city_object = self.parseCityString(location_string)
        CitySearchCache.objects.create(
            query = location_string.lower(),
            reference = city_object
        )

        return city_object




    def getLocationObjectByCityState(self,city,state):
        matching_location_objects = self.__search_object.by_city_and_state(city, state)
        if (len(matching_location_objects) == 0):
            raise ValueError

        return matching_location_objects[0]

    def _getZipByCityState(self,city,state):
        matching_location_object = self.getLocationObjectByCityState(city,state)
        zip_code = matching_location_object[0]['Zipcode']
        return zip_code


    def _getLatLongByZip(self,zip_code):
        location_object = self.__search_object.by_zipcode(zip_code)
        if(not location_object):
            return None
        return (location_object.Latitude, location_object.Longitude)

    def _getZipCodesNear(self,zip_code,radius_in_miles=15):
        try:
            (latitude,longitude) = self._getLatLongByZip(zip_code)
        except TypeError:
            return []

        locations_in_radius = self.__search_object.by_coordinate(latitude,longitude,radius=radius_in_miles,returns=0)

        return set([location.pk for location in locations_in_radius])
