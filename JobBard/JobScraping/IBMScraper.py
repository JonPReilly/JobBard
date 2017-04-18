from .AbstractJobScraper import AbstractJobScraper
from .JsonScraper import JsonScraper


class IBMScraper(JsonScraper):
    def __init__(self):
        self.type = "Greenhouse"
        self.scrape_url = "https://www.greenhouse.io/"
        self.scrape_format = "json"
        self.canScrapeExperience = False
        self.canGetExperience = False
        self.scrape_method = 'POST'
        self.scrape_pattern = {
            'job': 'jobs',
            'company': 'DNE',
            'url': 'absolute_url',
            'title': 'title',
            'location': 'location',
            'city': 'DNE',
            'state': 'DNE',
            'keywords': 'DNE',
            "description": "DNE",
            'date_published': 'updated_at',
            'experience': 'DNE'

        }

        self.scrape_querey = {

        }

    def openUrl(self, url=None, header=None):
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
        AbstractJobScraper.openUrl(self, url=url, headers={'Accept': 'application/json'}, form_data=form)
