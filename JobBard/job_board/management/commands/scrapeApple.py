from JobScraping.AppleScraper import AppleScraper
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Loads jobs from files into DB"

    def handle(self, *args, **options):

        urls = [
            "https://jobs.apple.com/us/search/search-result",

        ]
        apScraper = AppleScraper()

        for url in urls:
            for page in range(3):
                print("Scraping: ", url, "(page {0})".format(page))
                apScraper.changeScrapePage(page)

                apScraper.openUrl(url)
                apScraper.scrape()
