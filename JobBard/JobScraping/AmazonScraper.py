from .JsonScraper import JsonScraper


class AmazonScraper(JsonScraper):
    def __init__(self):
        self.type = "Amazon"
        self.scrape_url = "https://www.amazon.jobs/en/search?base_query=software&loc_query=US&job_count=100&result_limit=100&sort=recent&cache"
        self.scrape_format = "json"
        self.canScrapeExperience = False
        self.canGetExperience = True
        self.scrape_pattern = {
            'job': 'jobs',
            'company': 'company_name',
            'url': 'url_next_step',
            'title': 'title',
            'location': ('city', 'state'),
            'city': 'city',
            'state': 'state',
            'keywords': 'DNE',
            "description": "description",
            'date_published': 'posted_date',
            'experience': 'basic_qualifications'

        }

        self.scrape_querey = {

        }
