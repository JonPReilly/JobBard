from datetime import datetime

from .AbstractJobScraper import AbstractJobScraper

class StackOverflowScraper(AbstractJobScraper):
    def __init__(self):
        self.type = "STACKOVERFLOW"
        self.scrape_url = "http://stackoverflow.com/jobs/feed?l=united%20states"
        self.scrape_format = "xml"
        self.canScrapeExperience = False
        self.scrape_pattern = {
            "job": "item",
            "title": "title",
            "keywords": "category",
            "company": "name",
            "location": "location",
            "description": "description",
            "date_published": "pubDate",
            "date_updated": "updated",
            "url": "link"
        }
        self.scrape_querey = {
            "location": "location",
            "search": "q"
        }

    def parseDate(self, dateString):
        return datetime.strptime(dateString + " UTC", '%a, %d %b %Y %H:%M:%S Z %Z')
