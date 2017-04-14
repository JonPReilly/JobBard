from datetime import datetime

from .AbstractJobScraper import AbstractJobScraper


class SalesforceScraper(AbstractJobScraper):
    def __init__(self):
        self.type = "Salesforce"
        self.scrape_url = "http://salesforce.careermount.com/candidate/job_search/quick/results?location=Us&keyword=Software&relevance=true&sort_dir=desc&sort_field=post_date&rss"
        self.scrape_format = "xml"
        self.scrape_method = "GET"
        self.canScrapeExperience = False
        self.scrape_pattern = {
            "job": "item",
            "title": "title",
            "keywords": "DNE",
            "company": "DNE",
            "location": "location",
            "description": "description",
            "date_published": "DNE",
            "date_updated": "DNE",
            "url": "link"
        }

    def parseDate(self, dateString):
        return datetime.strptime(dateString + " UTC", ' Date posted: %m/%d/%Y %Z')

    def getJobLocation(self, job):
        full_description = AbstractJobScraper.getJobDescription(self, job)
        location = full_description.split('<br />')[0].split('-')
        try:
            state = location[1].strip()
            city = location[2].replace('(HQ)', '').strip()
        except IndexError:
            city = "Unknown"
            state = "Unknown"
        return city + "," + state

    def getPostedDate(self, job):
        full_description = AbstractJobScraper.getJobDescription(self, job)
        return full_description.split('<br />')[3]

    def getJobDescription(self, job):
        full_description = AbstractJobScraper.getJobDescription(self, job)
        return full_description.split('<br />')[1]

    def getCompany(self, job):
        return self.type
