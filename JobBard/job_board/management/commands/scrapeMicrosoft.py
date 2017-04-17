import time

from JobScraping.MicrosoftScraper import MicrosoftScraper
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Scrapes Microsoft Jobs"

    def handle(self, *args, **options):
        CLICK_NEXT_TIMES = 4
        NUM_PAGES_TO_SCRAPE = CLICK_NEXT_TIMES + 1  # Initial page + number of pages we click next
        url = "https://careers.microsoft.com/search.aspx"
        msScraper = MicrosoftScraper()
        msScraper.openUrl(url)
        for x in range(NUM_PAGES_TO_SCRAPE):
            print("Scraping...")
            msScraper.scrape()
            if (x < CLICK_NEXT_TIMES):
                print("Clicking next page...")
                msScraper.clickNextPage()
                time.sleep(40)

        msScraper.closeWebDriver()
