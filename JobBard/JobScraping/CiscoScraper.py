from .AbstractJobScraper import AbstractJobScraper


class CiscoScraper(AbstractJobScraper):
    def __init__(self):
        self.type = "Cisco"
        self.scrape_url = ""
        self.scrape_format = "html.parser"
        self.canScrapeExperience = False
        self.scrape_pattern = {
            'job': 'tr',
            'url': 'a',
            'title': 'Job Title',
            'location': 'Location',
            'keywords': 'DNE',
            "description": "job-search-content",
            'date_published': 'DNE'

        }

        self.scrape_querey = {
        }

    def getAllJobs(self):
        return self.soupObject.find("table", class_="table_basic-1 table_striped").find("tbody").find_all("tr")

    def getJobLocation(self, job):
        return self.extractFromEncoding(job.find("td", {'data-th': self.scrape_pattern['location']})).replace(", US",
                                                                                                              "")

    def getJobDescription(self, job):
        return ""

    def getJobTitle(self, job):
        return self.extractFromEncoding(job.find("td", {'data-th': self.scrape_pattern['title']}))

    def getJobUrl(self, job):
        return job.find("a")['href']

    def getCompany(self, job):
        return self.type
