# view-source:http://www.facebook.jobs/jobs/?q=Software+Engineer&sort=date&location=United+States#7
from .AbstractJobScraper import AbstractJobScraper


class FacebookScraper(AbstractJobScraper):
    def __init__(self):
        self.type = "Facebook"
        self.scrape_url = ""
        self.scrape_format = "html.parser"
        self.canScrapeExperience = False
        self.scrape_pattern = {
            'job': 'direct_joblisting with_description',
            'url': 'a',
            'title': 'resultHeader',
            'location': 'Location',
            'location_city': 'addressLocality',
            'location_state': 'addressRegion',
            'keywords': 'DNE',
            'description': "directseo_jobsnippet",
            'date_published': 'DNE'

        }

        self.scrape_querey = {
        }

    def getCompany(self, job):
        return self.type

    def getAllJobs(self):
        return self.soupObject.find_all("li", class_=self.scrape_pattern['job'])

    def getJobUrl(self, job):
        base_url = 'http://www.facebook.jobs/'
        job_url_extension = job.find("a")['href']
        return base_url + job_url_extension

    def getJobDescription(self, job):
        return ""

    def getJobTitle(self, job):
        return self.extractFromEncoding(job.find('span', class_=self.scrape_pattern['title']))

    def getJobLocation(self, job):
        city = self.extractFromEncoding(job.find('span', {'itemprop': self.scrape_pattern['location_city']}))
        state = self.extractFromEncoding(job.find('span', {'itemprop': self.scrape_pattern['location_state']}))
        if (state == None):
            state = self.extractFromEncoding(job.find('span', {'itemprop': 'addressCountry'}))
        return city + "," + state
