# https://api.greenhouse.io/v1/boards/slack/jobs
import time
from django.core.management.base import BaseCommand,CommandError
from JobScraping.GreenhouseScraper import GreenhouseScraper
import random
import os

class Command(BaseCommand):
    help = "Loads jobs from files into DB"

    def handle(self, *args, **options):

        urls = [
            ("https://api.greenhouse.io/v1/boards/lookout/jobs", 'Lookout'),
            ("https://api.greenhouse.io/v1/boards/digitalocean98/jobs", 'DigitalOcean'),
            ("https://api.greenhouse.io/v1/boards/tripadvisor/jobs", 'TripAdvisor'),
            ("https://api.greenhouse.io/v1/boards/slack/jobs" , 'Slack') ,
            ("https://api.greenhouse.io/v1/boards/fitbit92/jobs", 'Fitbit'),
            ("https://api.greenhouse.io/v1/boards/airbnb/jobs", 'Airbnb'),
            ("https://api.greenhouse.io/v1/boards/evernote/jobs", 'Evernote'),
            ("https://api.greenhouse.io/v1/boards/twilio/jobs", 'Twilio'),
            ("https://api.greenhouse.io/v1/boards/pinterest/jobs", 'Pinterest'),
            ("https://api.greenhouse.io/v1/boards/vimeo/jobs", 'Vimeo'),
            ("https://api.greenhouse.io/v1/boards/surveymonkey/jobs", 'Surveymonkey'),
            ("https://api.greenhouse.io/v1/boards/docusign/jobs", 'Docusign'),
            ("https://api.greenhouse.io/v1/boards/casper/jobs", 'Casper'),
            ("https://api.greenhouse.io/v1/boards/greenhouse/jobs", 'Greenhouse'),
            ("https://api.greenhouse.io/v1/boards/metromile/jobs", 'Metromile'),
            ("https://api.greenhouse.io/v1/boards/squarespace/jobs", 'Squarespace'),
            ("https://api.greenhouse.io/v1/boards/snapchat/jobs", 'Snapchat'),
            ("https://api.greenhouse.io/v1/boards/shazam/jobs", 'Shazam'),
            ("https://api.greenhouse.io/v1/boards/tumblr/jobs", 'Tumblr'),
            ("https://api.greenhouse.io/v1/boards/nerdwallet/jobs", 'Nerdwallet'),
            ("https://api.greenhouse.io/v1/boards/buzzfeed/jobs", 'Buzzfeed'),
            ("https://api.greenhouse.io/v1/boards/thumbtack/jobs", 'Thumbtack'),
            ("https://api.greenhouse.io/v1/boards/uber/jobs", 'Uber'),



        ]
        random.shuffle(urls)
        ghScraper = GreenhouseScraper()
        #input_file = "C:\\Users\Jon\Desktop\JobJolt\Code\JobJolt\JobBard\jobboard\scrape_tests/greenhouse-Fitbit.json"
        #print(input_file)
        #ghScraper.openFile(input_file)
        #ghScraper.type = 'Fitbit'
        #ghScraper.scrape()

        for url in urls:
            print("Scraping: " , url[0] , "for " , url[1])
            ghScraper.type = url[1]
            ghScraper.openUrl(url[0])
            ghScraper.scrapeUrl(url[0])
            time.sleep(10)
