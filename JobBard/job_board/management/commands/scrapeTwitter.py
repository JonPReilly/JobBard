from JobScraping.TwitterScraper import TwitterScraper
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Loads jobs from files into DB"

    def handle(self, *args, **options):
        url = "https://careers.twitter.com/content/careers-twitter/en/jobs-search.html?q=software&start="
        urls = []
        for x in range(5):
            urls.append(url + str(x*10))

        twitterScraper = TwitterScraper()

        for u in urls:
           print("Scraping: " + u)
           twitterScraper.openUrl(u)
           twitterScraper.scrape()
