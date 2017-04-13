import random
import time

from JobScraping.LeverScraper import LeverScraper
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Loads jobs from files into DB"

    def handle(self, *args, **options):
        urls = [
            ("https://jobs.lever.co/yelp/", 'Yelp'),
            ("https://jobs.lever.co/lyft/", 'Lyft'),
            ("https://jobs.lever.co/shopify/", 'Shopify'),
            ("https://jobs.lever.co/netflix/", 'Netflix'),
            ("https://jobs.lever.co/quora/", 'Quora'),
            ("https://jobs.lever.co/addepar/", 'Addepar'),
            ("https://jobs.lever.co/getaround/", 'Getaround'),
            ("https://jobs.lever.co/eventbrite/", 'Eventbrite'),
            ("https://jobs.lever.co/21/", '21'),
            ("https://jobs.lever.co/brigade/", 'Brigade'),
            ("https://jobs.lever.co/carbon/", 'Carbon'),
            ("https://jobs.lever.co/chexology/", 'Chexology'),
            ("https://jobs.lever.co/codefights/", 'Codefights'),
            ("https://jobs.lever.co/cruise/", 'Cruise'),
            ("https://jobs.lever.co/fictiv/", 'Fictiv'),
            ("https://jobs.lever.co/lever/", 'Lever'),
            ("https://jobs.lever.co/luxe/", 'Luxe'),
            ("https://jobs.lever.co/shopco/", 'Shop.co'),
            ("https://jobs.lever.co/twitch/", 'Twitch'),
            ("https://jobs.lever.co/coursera/", 'Coursera'),
            ("https://jobs.lever.co/button/", 'Button'),
            ("https://jobs.lever.co/foursquare/", 'Foursquare'),
            ("https://jobs.lever.co/etsy/", 'Etsy'),
            ("https://jobs.lever.co/duolingo/", 'Duolingo'),

        ]
        random.shuffle(urls)
        levScraper = LeverScraper()
        for url in urls:
            print("Scraping: ", url[0], "for ", url[1])
            levScraper.type = url[1]
            levScraper.openUrl(url[0])
            levScraper.scrape()
            time.sleep(10)
