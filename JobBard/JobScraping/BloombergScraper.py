from datetime import datetime

from .JsonScraper import JsonScraper


class BloombergScraper(JsonScraper):
    def __init__(self):
        self.type = "Bloomberg"
        self.scrape_url = "https://careers.bloomberg.com/job_search/search_query?searchQueryString=nr%3D80%26qf%3DSoftware%26lc%3DNew%2BYork%26lc%3DPrinceton%26sd%3DSoftware%2BDeveloper%252FEngineering%26sd%3DEngineering%26sd%3DData%2BTechnology%2BSupport%252F%2BOther%26sd%3DProduct%2BDevelopment%26sd%3DSystems%252F%2BNetwork%2BEngineering%26sd%3DTechnical%2BSupport"
        self.scrape_format = "json"
        self.canScrapeExperience = False
        self.canGetExperience = False
        self.scrape_pattern = {
            'job': 'jobData',
            'company': 'DNE',
            'url': 'JobReqNbr',
            'title': 'JobTitle',
            'location': 'City',
            'city': 'City',
            'state': 'State',
            'keywords': 'DNE',
            "description": "DNE",
            'date_published': 'PostedDate',
            'experience': 'DNE'

        }

        self.scrape_querey = {

        }

    def getJobUrl(self, job):
        return "https://careers.bloomberg.com/job/detail/" + JsonScraper.getJobUrl(self, job)

    def parseDate(self, dateString):
        return datetime.strptime(dateString[:10] + " UTC", '%Y-%m-%d %Z')

    def openUrl(self, url=None, header=None):
        return JsonScraper.openUrl(self, url=url, header={'X-Requested-With': 'XMLHttpRequest'})

    def getCompany(self, job):
        return self.type

    def getJobDescription(self, job):
        return ""

    def getJobLocation(self, job):
        job = job['Office']
        city = job[
            self.scrape_pattern['city']
        ]
        state = job[
            self.scrape_pattern['state']
        ]

        if (state is not None and city is not None):
            return city + "," + state
        return city if state is None else state
