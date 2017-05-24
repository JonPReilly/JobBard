from uszipcode import ZipcodeSearchEngine
from location.models import City, State, Location



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


    def getOrCreate(self,city,state):

        try:
            location_object = self.getLocationObjectByCityState(city,state)
            zip_code = location_object.Zipcode or "Unknown"
            city_true_name = location_object.City or city
            state_true_name = location_object.State or state
            city_model, city_created = City.objects.get_or_create(name=city_true_name, zip_code=zip_code)
            state_model, state_created = State.objects.get_or_create(name=state_true_name.title())
            location_model, location_created = Location.objects.get_or_create(city=city_model,state=state_model)
        except ValueError:
            city_model, city_created = City.objects.get_or_create(name=city, zip_code="Invalid")
            state_model, state_created = State.objects.get_or_create(name=state)
            location_model, location_created = Location.objects.get_or_create(city=city_model, state=state_model)

        return location_model



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
