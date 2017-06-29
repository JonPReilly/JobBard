from .models import *
from location.models import *
from location.LocationManager import LocationManager


class JobSearcher:

    def __init__(self):
        self.MAX_SEARCH_RESULTS = 150

    def limitResults(self,quereyset):
        return quereyset[:self.MAX_SEARCH_RESULTS]

    def getAllJobs(self):
        return Job.objects.all()

    def getJobsAddedToday(self):
        today = datetime.today()
        t = today.replace(hour=0, minute=0, second=0)
        return Job.objects.filter(date_created__gte=t).order_by('-date_created')

    
    def getJobsFromCompany(self, company_quereyset):
        return Job.objects.filter(company__in = company_quereyset).order_by('-date_created')

    def getJobsInCity(self, cities):
        return Job.objects.filter(city__in=cities).order_by('-date_created')

    def getJobsInCityRadius(self,city,radius=15):
        locManager = LocationManager()
        close_cities = locManager.getCloseCities(city.zip_code)
        return Job.objects.filter(city__in=close_cities).order_by('-date_created')