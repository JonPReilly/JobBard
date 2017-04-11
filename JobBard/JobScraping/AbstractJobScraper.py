import json

from abc import ABC, abstractmethod
from bs4 import BeautifulSoup

class AbstractJobScraper(ABC):
    type = "Abstract"
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    scrape_url = ""
    scrape_method = "GET"
    scrape_pattern = {}
    scrape_querey = {}
    scrape_format = ""
    soupObject = None
    canScrapeExperience = False
    canGetExperience = False

    @abstractmethod
    def openFile(self,file):
        if(self.scrape_format is not 'json'):
            self.soupObject = BeautifulSoup(open(file, encoding="utf8"), self.scrape_format)
        else:
            self.soupObject = json.load(open(file, encoding="utf8"))


