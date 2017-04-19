import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from .RenderedScraper import RenderedScraper


class MicrosoftScraper(RenderedScraper):
    def __init__(self):
        RenderedScraper.__init__(self)
        self.web_driver_timeout_seconds = 40
        self.web_driver_explicit_load_condition = False
        self.type = "Microsoft"
        self.scrape_url = ""
        self.scrape_format = "HTML"
        self.canScrapeExperience = False
        self.scrape_pattern = {
            'job': 'Result',
            'url': 'sr-title text',
            'date_published': 'DNE',
            'company': 'title',
            'title': 'sr-title text',
            'location': 'width: 22%;',
            'keywords': 'DNE',
            "description": "text-align: justify",

        }

        self.scrape_querey = {
            "location": "l",
            "search": "description"
        }

    def getCompany(self, job):
        return self.type

    def clickNextPage(self):
        self.web_driver.execute_script("document.getElementsByClassName('commandNext')[0].click()")
        page_content = self.pullContentFromPage()
        self.loadScrapeObject(page_content)

    def prepareSearchPage(self):
        SEARCH_QUEREY = "software and not Product"
        KEYWORD_INPUT_SOFTWARE_JS = "$('#ContentPlaceHolder1_srSearch_search_txtKeywords').val('" + SEARCH_QUEREY + "')"
        LOCATION_INPUT_US_JS = "$('#ContentPlaceHolder1_srSearch_search_msdRegion_txtMultiSelect').val('United States')"
        CLICK_SEARCH_BUTTON_JS = "$('#ContentPlaceHolder1_srSearch_search_btnSearch').click()"

        SORT_BY_DATE_POSTED_JS = "document.getElementById('ContentPlaceHolder1_srSearchResults_lvSearchResults_lnkbtnSortByPublicationStartDate').click()"
        js_commands = [
            KEYWORD_INPUT_SOFTWARE_JS,
            LOCATION_INPUT_US_JS,
            CLICK_SEARCH_BUTTON_JS,
        ]
        for command in js_commands:
            print("Executing: ", command)
            self.web_driver.execute_script(command)
            time.sleep(2)

        self.waitUntilResultsLoaded()
        self.web_driver.execute_script(SORT_BY_DATE_POSTED_JS)
        print("Sorting by date...waiting 30 seconds")
        time.sleep(30)

    def preparePageForReading(self):
        self.prepareSearchPage()

    def getPageContent(self, url, request_headers, form_data, manual_close=False):
        return super().getPageContent(url, request_headers, form_data, manual_close=True)

    def waitUntilResultsLoaded(self):
        WebDriverWait(self.web_driver, self.web_driver_timeout_seconds).until(
            expected_conditions.element_to_be_clickable(
                (By.ID, "ContentPlaceHolder1_srSearchResults_lvSearchResults_lnkbtnSortByPublicationStartDate"))
        )

    def getAllJobs(self):
        print("Number of jobs: ", len(self.soupObject.find_all("div", class_=self.scrape_pattern['job'])))
        return self.soupObject.find_all("div", class_=self.scrape_pattern['job'])

    def getJobUrl(self, job):
        base_url = 'https://careers.microsoft.com/'
        extended_url = job.find("a")['href']
        return base_url + extended_url

    def getJobTitle(self, job):
        job_title = self.extractFromEncoding(job.find("a"))
        return job_title.strip()

    def getJobDescription(self, job):
        return self.extractFromEncoding(job.find("span", {'style': self.scrape_pattern['description']})).strip()

    def getJobLocation(self, job):
        full_location = self.extractFromEncoding(job.find("div", {'style': self.scrape_pattern['location']})).strip()
        location_sections = full_location.split("(")
        try:
            city = location_sections[0]
            state = location_sections[1].replace(")", "")
        except IndexError:
            city = location_sections[0]
            state = "Unknown"

        return city + "," + state
