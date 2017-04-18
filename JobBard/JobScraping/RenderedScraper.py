from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from .AbstractJobScraper import AbstractJobScraper


class RenderedScraper(AbstractJobScraper):
    def __init__(self):
        self.web_driver = webdriver.Chrome()
        self.web_driver_timeout_seconds = 10
        self.web_driver_explicit_load_condition = False

    def closeWebDriver(self):
        self.web_driver.quit()
        self.web_driver = None

    def initWebDriver(self):
        if (self.web_driver == None):
            self.web_driver = webdriver.Chrome()

    def waitUntilJSLoaded(self):
        WebDriverWait(self.web_driver, self.web_driver_timeout_seconds).until(
            expected_conditions.element_to_be_clickable((By.ID, "gjsrpn"))
        )

    def implicitlyWait(self):
        self.web_driver.implicitly_wait(self.web_driver_timeout_seconds)
    def getPageAndWaitForLoad(self, url):
        if (not self.web_driver_explicit_load_condition):
            self.implicitlyWait()
        self.web_driver.get(url)
        if (self.web_driver_explicit_load_condition):
            self.waitUntilJSLoaded()

    def preparePageForReading(self):
        return

    def pullContentFromPage(self):
        page_content = self.web_driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
        return page_content

    # TODO: Edit Request headers and form data? It is highly unlikely this is needed.
    def getPageContent(self, url, request_headers, form_data, manual_close=False):
        self.initWebDriver()
        self.getPageAndWaitForLoad(url)
        self.preparePageForReading()
        page_content = self.pullContentFromPage()
        if (not manual_close):
            self.closeWebDriver()
        return page_content
