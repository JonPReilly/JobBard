from datetime import datetime

from .JsonScraper import JsonScraper


class GreenhouseScraper(JsonScraper):
    def __init__(self):
        self.type = "Greenhouse"
        self.scrape_url = "https://www.greenhouse.io/"
        self.scrape_format = "json"
        self.canScrapeExperience = False
        self.canGetExperience = False
        self.scrape_pattern = {
            'job': 'jobs',
            'company': 'DNE',
            'url': 'absolute_url',
            'title': 'title',
            'location': 'location',
            'city': 'DNE',
            'state': 'DNE',
            'keywords': 'DNE',
            "description": "DNE",
            'date_published': 'updated_at',
            'experience': 'DNE'

        }

        self.scrape_querey = {

        }

    def abstract(self):
        return False

    def getJobLocation(self, job):
        return job[
            self.scrape_pattern['location']
        ]['name']

    def getCompany(self, job):
        return self.type

    def getJobDescription(self, job):
        return ""

    def parseDate(self, dateString):
        try:

            return datetime.strptime(dateString[:18] + " UTC", '%Y-%m-%dT%H:%M:%S %Z')
        except ValueError:
            return datetime.now()