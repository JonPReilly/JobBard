from datetime import datetime

from .AbstractJobScraper import AbstractJobScraper


class TwitterScraper(AbstractJobScraper):
    def __init__(self):
        self.type = "Twitter"
        self.scrape_url = "https://careers.twitter.com/content/careers-twitter/en/jobs-search.html?q=software&start="
        self.scrape_format = "html.parser"
        self.canScrapeExperience = False
        self.scrape_pattern = {
            'job': 'job-search-item accordion-content-link js-results-list__item',
            'url': 'a',
            'title': 'job-search-title',
            'location': 'col info',
            'keywords': 'DNE',
            "description": "job-search-content",
            'date_published': 'DNE'

        }

        self.scrape_querey = {
            "location": "location",
            "search": "q",
            "pageation": 'start'
        }

    def getCompany(self, job):
        return self.type

    def getJobUrl(self, job):
        return job.find(self.scrape_pattern["url"])['href']

    def getAllJobs(self):
        return self.soupObject.find_all("li", class_=self.scrape_pattern['job'])

    def getJobTitle(self, job):
        return job.find_all("h4", class_=self.scrape_pattern['title'])[0].get_text()

    def getJobLocation(self, job):
        return job.find_all("div", class_=self.scrape_pattern['location'])[1].get_text()

    def getJobDescription(self, job):
        return job.find_all("div", class_=self.scrape_pattern['description'])[0].get_text().replace("\n", "")

    def parseDate(self, dateString):
        return datetime.now()