from JobScraping.BloombergScraper import BloombergScraper
from django.core.management.base import BaseCommand


# TODO: Bloomberg urls change a lot and return 404. See if this can be prevented. Possibly something with cookies
class Command(BaseCommand):
    help = "Loads jobs from files into DB"

    def handle(self, *args, **options):
        urls = [
            "https://careers.bloomberg.com/job_search/search_query?autocompleteTags=%5B%7B%22value%22%3A%22Software+Engineer%22%2C%22isManuallyAdded%22%3Atrue%2C%22creationTimestamp%22%3A1492209677%7D%5D&selectedFilterFields=%5B%5D&jobStartIndex=0&jobBatchSize=20&_csrf=2KDwTfjaZkce20h7dZoSwl%2BoTl5qFqBpks8vs%3D"
        ]
        BbScraper = BloombergScraper()

        for url in urls:
            print("Scraping: ", url)
            BbScraper.openUrl(url)
            BbScraper.scrape()
