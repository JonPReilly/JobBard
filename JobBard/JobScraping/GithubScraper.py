from datetime import datetime

from .AbstractJobScraper import AbstractJobScraper


class GithubScraper(AbstractJobScraper):
    def __init__(self):
        self.type = "GITHUB"
        self.scrape_url = "https://jobs.github.com/positions.atom?full_time=on"
        self.scrape_format = "xml"
        self.canScrapeExperience = False
        self.scrape_pattern = {
            'job': 'entry',
            'url': 'link',
            'date_published': 'updated',
            'company': 'title',
            'title': 'title',
            'location': 'title',
            'keywords': 'DNE',
            "description": "content",

        }

        self.scrape_querey = {
            "location": "l",
            "search": "description"
        }

    def getCompany(self, job):
        return AbstractJobScraper.getCompany(self, job).split(" at ")[1].split(" in")[0].replace(" ", "")

    def getJobTitle(self, job):
        return AbstractJobScraper.getJobTitle(self, job).split(" at ")[0]

    def getJobLocation(self, job):
        loc = AbstractJobScraper.getJobLocation(self, job).split(" in")[1]
        if ("," not in loc):
            loc = loc + ", "
        return loc

    def getKeywords(self, job):
        return []

    def parseDate(self, dateString):
        return datetime.strptime(dateString + " UTC", '%Y-%m-%dT%H:%M:%SZ %Z')

    def getJobUrl(self, job):
        return job.find(self.scrape_pattern["url"])['href']
