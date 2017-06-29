import re

from django.db.models import Q

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

    def normalize_query(self, search_querey):
        return search_querey.split(" ")

    def get_query(self,query_string, search_fields):
        query = None  # Query to search for every search term
        terms = self.normalize_query(query_string)
        for term in terms:
            or_query = None  # Query to search for a given term in each field
            for field_name in search_fields:
                q = Q(**{"%s__icontains" % field_name: term})
                if or_query is None:
                    or_query = q
                else:
                    or_query = or_query | q
            if query is None:
                query = or_query
            else:
                query = query & or_query
        return query


    def searchJobs(self,search_querey):
        JOB_SEARCH_FIELDS = ('title','company__name')
        FINAL_QUERY = self.get_query(search_querey,JOB_SEARCH_FIELDS)

        print(FINAL_QUERY)
        return Job.objects.filter(
            FINAL_QUERY
        ).order_by('-date_created')