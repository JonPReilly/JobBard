from datetime import datetime

from .AbstractJobScraper import AbstractJobScraper


class LeverScraper(AbstractJobScraper):
    def __init__(self):
        self.type = "Lever"
        self.scrape_url = "https://jobs.lever.co/"
        self.scrape_format = "html.parser"
        self.canScrapeExperience = False
        self.canGetExperience = False
        self.scrape_pattern = {
            'job': 'posting',
            'company': 'DNE',
            'url': 'a',
            'title': 'h5',
            'location': 'sort-by-location posting-category small-category-label',
            'city': 'DNE',
            'state': 'DNE',
            'keywords': 'DNE',
            "description": "DNE",
            'date_published': 'DNE',
            'experience': 'DNE'

        }
        self.scrape_querey = {

        }

    def getCompany(self, job):
        return self.type

    def getAllJobs(self):
        return self.soupObject.find_all("div", class_=self.scrape_pattern['job'])

    def parseDate(self, dateString):
        return datetime.now()

    def getJobTitle(self, job):
        return (job.find(self.scrape_pattern['title']).get_text())

    def getJobLocation(self, job):
        try:
            location = (job.find("span", class_=self.scrape_pattern['location']).get_text())
        except AttributeError:
            location = "Unknown, Unknown"
        return location

    def getJobUrl(self, job):
        return job.find(self.scrape_pattern["url"])['href']
