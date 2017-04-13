from JobScraping.AmazonScraper import AmazonScraper
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Loads jobs from files into DB"

    def handle(self, *args, **options):
        urls = [
            "https://www.amazon.jobs/en/search?base_query=&loc_query=&job_count=10&result_limit=10&sort=relevant&category%5B%5D=software-development&cache",
            "https://www.amazon.jobs/en/search?base_query=&loc_query=&job_count=10&result_limit=10&sort=relevant&category%5B%5D=systems-quality-security-engineering&cache",
            "https://www.amazon.jobs/en/search?base_query=&loc_query=&job_count=10&result_limit=10&sort=relevant&category%5B%5D=database-administration&cache",
            "https://www.amazon.jobs/en/search?base_query=software&loc_query=&job_count=100&result_limit=100&sort=recent&location%5B%5D=bostoncambridge-area-ma&cache",
            "https://www.amazon.jobs/en/search?base_query=software&loc_query=Boston&job_count=100&result_limit=100&sort=recent&location%5B%5D=palo-alto&location%5B%5D=san-francisco&location%5B%5D=sunnyvale-california&cache",
            "https://www.amazon.jobs/en/search?base_query=developer&loc_query=US&job_count=100&result_limit=100&sort=recent&cache&business_category%5B%5D=university-recruiting",
        ]
        amScraper = AmazonScraper()
        # input_file = "C:\\Users\Jon\Desktop\JobJolt\Code\JobJolt\JobBard\jobboard\scrape_tests/amazon.json"
        # print(input_file)
        # amScraper.openFile(input_file)
        # amScraper.scrape()

        for url in urls:
            print("Scraping: ", url)
            amScraper.openUrl(url)
            amScraper.scrape()
