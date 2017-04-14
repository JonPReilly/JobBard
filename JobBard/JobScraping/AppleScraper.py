from datetime import datetime

from .AbstractJobScraper import AbstractJobScraper


class AppleScraper(AbstractJobScraper):
    def __init__(self):
        self.type = "Apple Inc."
        self.scrape_url = "https://jobs.apple.com/us/search/search-result"
        self.scrape_format = "xml"
        self.scrape_method = "POST"
        self.canScrapeExperience = False
        self.scrape_pattern = {
            "job": "requisition",
            "title": "postingTitle",
            "keywords": "DNE",
            "company": "name",
            "location": "location",
            "description": "DNE",
            "date_published": "opendate",
            "date_updated": "updated",
            "url": "jobId"
        }
        self.form_data = {
            'csrfToken': 'null',
            'clientOffset': '-300',
            'searchRequestJson': '{"searchString":"","jobType":0,"filters":{"locations":{"location":[{"type":"0","code":"USA"}]},"retailJobSpecs":null,"businessLine":null,"jobFunctions":{"jobFunctionCode":["AIS","HDWEG","MIS","CGINT","SFWEG"]},"languageSkills":null,"hiringManagerId":null},"sortBy":"req_open_dt","sortOrder":"1","pageNumber":"0"}'
        }

    def openUrl(self, url=None, header=None, form=None):
        return AbstractJobScraper.openUrl(self, url=url, form_data=self.form_data)

    def parseDate(self, dateString):
        return datetime.strptime(dateString + " UTC", '%b. %d, %Y %Z')

    def getJobUrl(self, job):
        job_id = AbstractJobScraper.getJobUrl(self, job)
        url = "https://jobs.apple.com/us/search?job={0}&openJobId={0}#&openJobId={0}".format(job_id)
        return url

    def getCompany(self, job):
        return self.type

    def changeScrapePage(self, pageNum):
        new_dict = '{"searchString":"","jobType":0,"filters":{"locations":{"location":[{"type":"0","code":"USA"}]},"retailJobSpecs":null,"businessLine":null,"jobFunctions":{"jobFunctionCode":["AIS","HDWEG","MIS","CGINT","SFWEG"]},"languageSkills":null,"hiringManagerId":null},"sortBy":"req_open_dt","sortOrder":"1","pageNumber":"{{pageNum}}"}'.replace(
            "{{pageNum}}", str(pageNum))
        self.form_data['searchRequestJson'] = new_dict
