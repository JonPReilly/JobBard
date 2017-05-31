import time

from JobScraping.ZiprecruiterScraper import ZiprecruiterScraper
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Scrapes Twitter for jobs"

    def handle(self, *args, **options):
        url = "https://www.ziprecruiter.com/candidate/search?search={0}&location={1}&page={2}&no_header_footer=1&days=1"

        queries = ['software', 'developer','python', 'systems']
        locations = ['', 'boston', 'california', 'NY']
        urls = []

        for q in queries:
            for l in locations:
                for x in range(3):
                    urls.append(url.format(q,l,x))

        ziprecruiter_scraper = ZiprecruiterScraper()

        for u in urls:
           print("Scraping: " + u)
           ziprecruiter_scraper.openUrl(u)
           ziprecruiter_scraper.scrape()
           time.sleep(3)
