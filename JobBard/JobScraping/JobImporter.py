from job_board.models import Job, Company
from location.LocationManager import LocationManager


class JobImporter:
    def addJob(self,company_name,title,url,location,description="",required_experience="",years_experience=None,posted_date=None):
        if (self.jobExists(url)):
            return #Do nothing for now. Update the job object in the future?
        if (location == None):
            location = "Unknown, Unknown"
        company_object = self.getCompanyObject(company_name)
        location_object =  self.getLocationObject(location)

        Job.objects.get_or_create(
            title=title,
            description=description,
            url = url,
            company = company_object,
            location= location_object,
            required_experience = required_experience,
            years_experience_required=years_experience
        )



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
        city = loc[0].replace(" ", "")
        try:
            state = loc[1].replace(" ", "")
        except IndexError:
            state = ""

        locManager = LocationManager()
        return locManager.getOrCreate(city,state)
