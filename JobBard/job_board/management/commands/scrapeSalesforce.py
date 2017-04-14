from JobScraping.SalesforceScraper import SalesforceScraper
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Scrapes Salesforce"

    def handle(self, *args, **options):
        urls = [
            'http://salesforce.careermount.com/candidate/job_search/quick/results?location=Us&keyword=Software&relevance=true&sort_dir=desc&sort_field=post_date&rss',
            'http://salesforce.careermount.com/candidate/job_search/quick/results?location=Us&keyword=Technology&sort_dir=desc&sort_field=post_date&rss',
            'http://salesforce.careermount.com/candidate/job_search/quick/results?location=Us&keyword=database&sort_dir=desc&sort_field=post_date&rss',
            'http://salesforce.careermount.com/candidate/job_search/quick/results?location=Us&keyword=intern&sort_dir=desc&sort_field=post_date&rss',
            'http://salesforce.careermount.com/candidate/job_search/quick/results?location=Us&keyword=engineer&sort_dir=desc&sort_field=post_date&rss'
        ]
        sfScraper = SalesforceScraper()

        for url in urls:
            print("Scraping: ", url)
            sfScraper.openUrl(url)
            sfScraper.scrape()
