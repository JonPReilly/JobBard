from datetime import datetime
import json

from abc import ABC, abstractmethod
from bs4 import BeautifulSoup

import urllib.request
from urllib.parse import urlencode
from urllib.error import HTTPError,URLError
from JobScraping.JobImporter import JobImporter


class AbstractJobScraper(ABC):
    type = "Abstract"
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
    scrape_url = ""
    scrape_method = "GET"
    scrape_pattern = {}
    scrape_querey = {}
    scrape_format = "HTML"
    soupObject = None
    canScrapeExperience = False
    canGetExperience = False



    def openFile(self,file):
        if(self.scrape_format is not 'json'):
            self.soupObject = BeautifulSoup(open(file, encoding="utf8"), self.scrape_format)
        else:
            self.soupObject = json.load(open(file, encoding="utf8"))

    def getHeaders(self,headers):
        request_headers = {'User-Agent': self.user_agent}
        for key in headers:
            request_headers[key] = headers[key]
        return request_headers

    def openUrl(self,url, headers={},form_data={}):
        request_headers = self.getHeaders(headers)
        try:
            form_data = urlencode(form_data).encode('utf-8')
            page_content = urllib.request.urlopen(urllib.request.Request(url, headers=request_headers, method=self.scrape_method, data=form_data))
        except (URLError, HTTPError) as e:
            self.soupObject = BeautifulSoup("")
            return
        if (self.scrape_format is not 'json'):
            self.soupObject = BeautifulSoup(page_content.read(), self.scrape_format)
        else:
            content = page_content.read().decode('utf-8')
            self.soupObject = (json.loads(content))

    def scrape(self):
        jobs_added = 0
        if (self.soupObject == None):
            return jobs_added
        
        for job in self.getAllJobs():
            job_company_name = self.getCompany(job)
            job_title = self.getJobTitle(job)
            job_description = self.getJobDescription(job)
            job_url = self.getJobUrl(job)
            job_required_experience = self.getRequiredExperience(job)
            job_years_experience = self.getYearsExperience(job_required_experience)
            job_location = self.getJobLocation(job)
            job_posted_date = self.parseDate(self.getPostedDate(job))

            self.addJob(
                company_name=job_company_name,
                location=job_location,
                title=job_title,
                url=job_url,
                description=job_description,
                required_experience=job_required_experience,
                years_experience=job_years_experience,
                posted_date = job_posted_date
            )



    def scrapeUrl(self,url):
        self.openUrl(url)
        self.scrape()
    def scrapeFile(self,file):
        self.openFile(file)
        self.scrape()

    def getAllJobs(self):
        return self.soupObject.find_all(self.scrape_pattern["job"])

    def getJobTitle(self, job):
        return self.extractFromEncoding(job.find(self.scrape_pattern["title"]))

    def getCompany(self, job):
        return self.extractFromEncoding(job.find(self.scrape_pattern["company"]))

    def getJobDescription(self, job):
        return self.extractFromEncoding(job.find(self.scrape_pattern["description"]))

    def getJobUrl(self, job):
        return self.extractFromEncoding(job.find(self.scrape_pattern["url"]))

    def getRequiredExperience(self, job):
        return ""

    def getYearsExperience(self, job_required_experience):
        return None

    def addJob(self,company_name,title,url,location,description="",required_experience="",years_experience=None,posted_date=None):
        jobImporter = JobImporter()
        jobImporter.addJob(company_name,title,url,location,description,required_experience,years_experience,posted_date)

    def getJobLocation(self, job):
        return self.extractFromEncoding(job.find(self.scrape_pattern["location"]))

    def getPostedDate(self, job):
        return self.extractFromEncoding(job.find(self.scrape_pattern["date_published"]))

    def extractFromEncoding(self, encoded):
        return encoded.string if encoded != None else None

    def parseDate(self, dateString):
        return datetime.now()

