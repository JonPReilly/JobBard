import time

from JobScraping.IBMScraper import IBMScraper
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Loads jobs from files into DB"

    def handle(self, *args, **options):
        url = 'https://krb-sjobs.brassring.com/TgNewUI/Search/Ajax/ProcessSortAndShowMoreJobs'

        ibm_scraper = IBMScraper()
        NUM_PAGES_TO_SCRAPE = 3

        for x in range(NUM_PAGES_TO_SCRAPE):
            page_num = x + 1
            print("Scraping (Page {}): ".format(page_num), url)
            ibm_scraper.openUrl(url, page_number=page_num)
            ibm_scraper.scrape()
            time.sleep(15)
