from job_board.models import Job, Company
from location.LocationManager import LocationManager


class JobImporter:
    def addJob(self,company_name,title,url,location,description="",required_experience="",years_experience=None,posted_date=None):
        if (self.jobExists(url)):
            return #Do nothing for now. Update the job object in the future?
        if (location == None):
            return

        company_object = self.getCompanyObject(company_name.title())
        city_object =  self.getCityObject(location.replace("Unknown",""))
        if(city_object == None):
            return
        Job.objects.get_or_create(
            title=title,
            description=description,
            url = url,
            company = company_object,
            location= None,
            required_experience = required_experience,
            years_experience_required=years_experience,
            city = city_object
        )



    def getCityObject(self, location):
        locManager = LocationManager()
        return locManager.getCity(location)
    def jobExists(self,url):
        try:
            Job.objects.get(url=url)
        except Job.DoesNotExist:
            return False
        return True

    def getCompanyObject(self,company_name):
        company, created = Company.objects.get_or_create(name=company_name)
        return company

    def getLocationObject(self,location_string):
        if (location_string == None):
            return None
        loc = location_string.split(",")
        city = loc[0].replace(" ", "").title()
        try:
            state = loc[1].replace(" ", "").title()
        except IndexError:
            state = ""

        locManager = LocationManager()
        return locManager.getOrCreate(city,state)
