import time

from JobScraping.IBMScraper import IBMScraper
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Loads jobs from files into DB"

    def handle(self, *args, **options):
        urls = [
            'https://krb-sjobs.brassring.com/TgNewUI/Search/Ajax/MatchedJobs'
        ]
        ibm_scraper = IBMScraper()

        for url in urls:
            print("Scraping: ", url)
            ibm_scraper.openUrl(url)
            ibm_scraper.scrape()
            time.sleep(15)
