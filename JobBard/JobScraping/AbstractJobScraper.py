import json
import urllib.request
from abc import ABC
from datetime import datetime
from urllib.error import HTTPError,URLError
from urllib.parse import urlencode

from JobScraping.JobImporter import JobImporter
from bs4 import BeautifulSoup


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



    def loadScrapeObjectFromString(self,page_content):
        self.soupObject = BeautifulSoup(page_content.read(), self.scrape_format)

    def loadScrapeObjectFromJson(self,page_content):
        content = page_content.read().decode('utf-8')
        self.soupObject = (json.loads(content))

    def loadScrapeObject(self,page_content):
        if (self.scrape_format is not 'json'):
            self.loadScrapeObjectFromString(page_content)
        else:
            self.loadScrapeObjectFromJson(page_content)

    def getPageContent(self, url, request_headers, form_data):
        page_content = urllib.request.urlopen(
            urllib.request.Request(url, headers=request_headers, method=self.scrape_method, data=form_data))
        return page_content
    def openUrl(self,url, headers={},form_data={}):
        request_headers = self.getHeaders(headers)
        try:
            form_data = urlencode(form_data).encode('utf-8')
            page_content = self.getPageContent(url, request_headers, form_data)
        except (URLError, HTTPError) as e:
            self.soupObject = BeautifulSoup("")
            return
        self.loadScrapeObject(page_content)

    def getJobAttributes(self, job):
        job_attributes = {}
        job_attributes['job_company_name'] = self.getCompany(job)
        job_attributes['job_title'] = self.getJobTitle(job)
        job_attributes['job_description'] = self.getJobDescription(job)
        job_attributes['job_url'] = self.getJobUrl(job)
        job_attributes['job_required_experience'] = self.getRequiredExperience(job)
        job_attributes['job_years_experience'] = self.getYearsExperience(job_attributes['job_required_experience'])
        job_attributes['job_location'] = self.getJobLocation(job)
        job_attributes['job_posted_date'] = self.parseDate(self.getPostedDate(job))
        return job_attributes

    def scrape(self):
        jobs_added = 0
        if (self.soupObject == None):
            return jobs_added
        
        for job in self.getAllJobs():
            job_attributes = self.getJobAttributes(job)

            self.addJob(
                company_name=job_attributes['job_company_name'],
                location=job_attributes['job_location'],
                title=job_attributes['job_title'],
                url=job_attributes['job_url'],
                description=job_attributes['job_description'],
                required_experience=job_attributes['job_required_experience'],
                years_experience=job_attributes['job_years_experience'],
                posted_date = job_attributes['job_posted_date']
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

