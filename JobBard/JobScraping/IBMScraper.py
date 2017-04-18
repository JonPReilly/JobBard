from django.utils.datetime_safe import datetime

from .AbstractJobScraper import AbstractJobScraper
from .JsonScraper import JsonScraper


class IBMScraper(JsonScraper):
    def __init__(self):
        self.type = "IBM"
        self.scrape_url = "https://www.greenhouse.io/"
        self.scrape_format = "json"
        self.canScrapeExperience = False
        self.canGetExperience = False
        self.scrape_method = 'POST'
        self.scrape_pattern = {
            'job': 'Job',
            'company': 'DNE',
            'url': 'reqid',
            'title': 'jobtitle',
            'location': 'formtext27',
            'city': 'DNE',
            'state': 'DNE',
            'keywords': 'DNE',
            "description": "jobdescription",
            'date_published': 'lastupdated',
            'experience': 'DNE'

        }

        self.scrape_querey = {

        }

    def openUrl(self, url=None, header=None, page_number=0):
        form = {
            'keyword': 'software',
            'location': 'united states',
            'keywordCustomSolrFields': 'FORMTEXT12,FORMTEXT15,FORMTEXT24,FORMTEXT56,FORMTEXT2',
            'locationCustomSolrFields': 'FORMTEXT10,FORMTEXT13,FORMTEXT27,FORMTEXT2',
            'partnerId': 26059,
            'siteId': 5016,
            'facetfilterfields': '',
            'SortType': 'LastUpdated',
            'Latitude': 0,
            'Longitude': 0

        }
        if (page_number != 0):
            form['pageNumber'] = page_number
        AbstractJobScraper.openUrl(self, url=url, headers={'Accept': 'application/json'}, form_data=form)

    def getCompany(self, job):
        return self.type

    def getAllJobs(self):
        return self.soupObject['Jobs'][self.scrape_pattern['job']]

    def extractFromQuestions(self, job, question_name):
        for question in job['Questions']:
            if (question['QuestionName'] == question_name):
                return question['Value']
        return ""

    def getJobUrl(self, job):
        base_url = "https://krb-jobs.brassring.com/tgwebhost/jobdetails.aspx?jobId={}&PartnerId=26059&SiteId=5016&JobReqLang=1"
        job_id = self.extractFromQuestions(job, self.scrape_pattern['url'])
        return base_url.format(job_id)

    def getJobTitle(self, job):
        return self.extractFromQuestions(job,
                                         self.scrape_pattern['title']
                                         )

    def getJobLocation(self, job):
        city = self.extractFromQuestions(job, self.scrape_pattern['location'])
        state = "Unknown"
        return city + "," + state

    def getJobDescription(self, job):
        job_description = self.extractFromQuestions(job, self.scrape_pattern['description'])
        return job_description

    def getExperience(self, job):
        return ""

    def getPostedDate(self, job):
        return self.extractFromQuestions(job, self.scrape_pattern['date_published'])

    def parseDate(self, dateString):
        return datetime.strptime(dateString + " UTC", '%d-%b-%Y %Z')
