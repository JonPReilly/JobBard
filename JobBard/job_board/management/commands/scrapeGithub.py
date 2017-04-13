import time

from JobScraping.GithubScraper import GithubScraper
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Loads jobs from files into DB"

    def handle(self, *args, **options):
        urls = [
            "https://jobs.github.com/positions.atom?full_time=on",
            "https://jobs.github.com/positions.atom?full_time=on&l=boston",
            "https://jobs.github.com/positions.atom?full_time=on&l=new+york",
            "https://jobs.github.com/positions.atom?full_time=on&l=ca",
            "https://jobs.github.com/positions?description=software&location=&full_time=ons",
        ]
        ghScraper = GithubScraper()
        # input_file = "C:\\Users\Jon\Desktop\JobJolt\Code\JobJolt\JobBard\jobboard\scrape_tests/stackoverflow.xml"
        # print(input_file)
        # soScraper.openFile(input_file)
        # soScraper.scrape()

        for url in urls:
            print("Scraping: ", url)
            ghScraper.openUrl(url)
            ghScraper.scrape()
            time.sleep(2)
