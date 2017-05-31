from datetime import datetime
from .AbstractJobScraper import AbstractJobScraper

class ZiprecruiterScraper(AbstractJobScraper):
    def __init__(self):
        self.type = "ZipRecruiter"
        self.scrape_url = "https://www.ziprecruiter.com/candidate/search?search=Software&location=&page=0&no_header_footer=1&days=1"
        self.scrape_format = "HTML"
        self.canScrapeExperience = False
        self.scrape_pattern = {
            "job": "job_content",
            "title": "just_job_title",
            "keywords": "dne",
            "company": "t_org_link",
            "location": "t_location_link",
            "description": "description",
            "date_published": "pubDate",
            "date_updated": "updated",
            "url": "job_link t_job_link"
        }

    def getAllJobs(self):
        return self.soupObject.find_all("div", class_=self.scrape_pattern['job'])

    def getJobUrl(self, job):
        return job.find("a", class_=self.scrape_pattern['url'])['href']

    def getCompany(self, job):
        return self.extractFromEncoding(job.find("a", class_=self.scrape_pattern['company']))

    def getJobTitle(self, job):
        return self.extractFromEncoding(job.find("span", class_=self.scrape_pattern['title']))

    def getJobLocation(self, job):

        location = self.extractFromEncoding(job.find("a", class_=self.scrape_pattern['location']))
        if (location == None):
            return ""
        return location.replace("\n","").strip()