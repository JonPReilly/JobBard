import time

from JobScraping.CiscoScraper import CiscoScraper
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Loads jobs from files into DB"

    def handle(self, *args, **options):
        url = 'https://jobs.cisco.com/jobs/SearchJobs/Software?3_109_3=%5B%22169482%22%5D&projectOffset={}'

        cisco_scraper = CiscoScraper()
        PAGES_TO_SCRAPE = 3
        NUM_JOBS_PER_PAGE = 25
        for x in range(PAGES_TO_SCRAPE):
            offet = NUM_JOBS_PER_PAGE * x
            print("Scraping: (Page {})".format(x), url.format(offet))
            cisco_scraper.openUrl(url.format(offet))
            cisco_scraper.scrape()
            time.sleep(10)
