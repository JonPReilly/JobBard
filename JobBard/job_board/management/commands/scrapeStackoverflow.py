from JobScraping.StackOverflowScraper import StackOverflowScraper
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Loads jobs from files into DB"

    def handle(self, *args, **options):
        urls = [
            "http://stackoverflow.com/jobs/feed?l=united%20states",
            "http://stackoverflow.com/jobs/feed?l=boston",
            "http://stackoverflow.com/jobs/feed?l=NY",
            "http://stackoverflow.com/jobs/feed?l=CA",
            "http://stackoverflow.com/jobs/feed?q=grad&l=united%20states",
            "http://stackoverflow.com/jobs/feed?q=software&l=united%20states",
            "http://stackoverflow.com/jobs/feed?cl=Microsoft",
            "http://stackoverflow.com/jobs/feed?cl=Google"
        ]
        soScraper = StackOverflowScraper()
        for url in urls:
            print("Scraping: ", url)
            soScraper.openUrl(url)
            soScraper.scrape()
