from uszipcode import ZipcodeSearchEngine
from JobBard.location.models import  City, State, Location

class LocationManager:
    __search_object = ZipcodeSearchEngine()




    def getOrCreate(self,city,state):
        zip_code = self._getZipByCityState(city,state)
        city_model, city_created = City.objects.get_or_create(name=city, zip_code=zip_code)
        state_model, state_created = State.objects.get_or_create(name=state)

        location_model, location_created = Location.objects.get_or_create(city=city_model,state=state_model)

        return location_model



    def _getZipByCityState(self,city,state):
        matching_location_objects = self.__search_object.by_city_and_state(city,state)
        if (len(matching_location_objects) == 0):
            return None

        zip_code = matching_location_objects[0]['Zipcode']
        return zip_code


    def _getLatLongByZip(self,zip_code):
        location_object = self.__search_object.by_zipcode(zip_code)
        if(not location_object):
            return None
        return (location_object.Latitude, location_object.Longitude)

    def _getZipCodesNear(self,zip_code,radius_in_miles=15):
        try:
            (latitude,longitude) = self.getLatLongByZip(zip_code)
        except TypeError:
            return []

        locations_in_radius = self.__search_object.by_coordinate(latitude,longitude,radius=radius_in_miles)

        return [location.Zipcode for location in locations_in_radius]
