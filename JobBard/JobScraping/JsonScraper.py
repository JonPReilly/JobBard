from datetime import datetime

from .AbstractJobScraper import AbstractJobScraper

class JsonScraper(AbstractJobScraper):
    def openUrl(self, url=None, header=None):
        return AbstractJobScraper.openUrl(self, url=url, headers={'Accept': 'application/json'})

    def getAllJobs(self):
        return self.soupObject[
            self.scrape_pattern['job']
        ]

    def getKeywords(self, job):
        return []

    def getCompany(self, job):
        return job[
            self.scrape_pattern['company']
        ]

    def getJobUrl(self, job):
        return job[
            self.scrape_pattern['url']
        ]

    def getJobTitle(self, job):
        return job[
            self.scrape_pattern['title']
        ]

    def getLocation(self, job):
        city = job[
            self.scrape_pattern['city']
        ]
        state = job[
            self.scrape_pattern['state']
        ]

        if (state is not None and city is not None):
            return city + "," + state
        return city if state is None else state

    def getJobDescription(self, job):
        return job[
            self.scrape_pattern['description']
        ]

    def getPostedDate(self, job):
        return job[
            self.scrape_pattern['date_published']
        ]

    def parseDate(self, dateString):
        return datetime.strptime(dateString + " UTC", '%B %d, %Y %Z')

    def getExperience(self, job):
        return job[
            self.scrape_pattern['experience']
        ]