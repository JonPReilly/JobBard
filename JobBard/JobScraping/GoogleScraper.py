from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from .RenderedScraper import RenderedScraper


class GoogleScraper(RenderedScraper):
    def __init__(self):
        RenderedScraper.__init__(self)
        self.web_driver_explicit_load_condition = True
        self.type = "Google"
        self.scrape_url = ""
        self.scrape_format = "xml"
        self.canScrapeExperience = False
        self.scrape_pattern = {
            'job': 'http://schema.org/JobPosting',
            'url': 'sr-title text',
            'date_published': 'DNE',
            'company': 'title',
            'title': 'sr-title text',
            'location': 'location secondary-text',
            'keywords': 'DNE',
            "description": "DNE",

        }

        self.scrape_querey = {
            "location": "l",
            "search": "description"
        }

    def getJobUrl(self, job):
        base_url = 'https://careers.google.com/jobs'
        extended_url = job.find("a", class_=self.scrape_pattern['url'])['href']
        return base_url + extended_url

    def getAllJobs(self):
        return self.soupObject.find_all("div", attrs={'itemtype': self.scrape_pattern['job']})

    def getCompany(self, job):
        return self.type

    def waitUntilPagationExists(self):
        WebDriverWait(self.web_driver, self.web_driver_timeout_seconds).until(
            expected_conditions.element_to_be_clickable((By.ID, "gjsrpn"))
        )

    def waitUntilLowVolumeSearchExists(self):
        WebDriverWait(self.web_driver, self.web_driver_timeout_seconds).until(
            expected_conditions.element_to_be_clickable((By.ID, "cssnrft"))
        )

    def waitUntilJSLoaded(self):
        try:
            self.waitUntilPagationExists()
        except TimeoutException:
            self.waitUntilLowVolumeSearchExists()


    def getJobDescription(self, job):
        return ""

    def getJobTitle(self, job):
        return job.find("a", class_=self.scrape_pattern['title'])['title']

    def getJobLocation(self, job):
        return self.extractFromEncoding(job.find("span", class_=self.scrape_pattern["location"])).replace(", USA", "")
