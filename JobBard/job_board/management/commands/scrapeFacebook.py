import time

from JobScraping.FacebookScraper import FacebookScraper
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Loads jobs from files into DB"

    # TODO: Perhaps scroll, or hit http://www.facebook.jobs/ajax/titles/?offset=20&num_items=20&q=Software&location=United&filter_path=%2Fjobs%2F
    def handle(self, *args, **options):
        urls = [
            'http://www.facebook.jobs/jobs/?q=Software+Engineer&sort=date&location=United+States#7'
        ]
        facebook_scraper = FacebookScraper()

        for url in urls:
            print("Scraping: ", url)
            facebook_scraper.openUrl(url)
            facebook_scraper.scrape()
            time.sleep(2)
