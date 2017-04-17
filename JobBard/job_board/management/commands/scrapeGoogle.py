import time

from JobScraping.GoogleScraper import GoogleScraper
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Loads jobs from files into DB"

    def handle(self, *args, **options):
        urls = [
            # 'https://careers.google.com/jobs#t=sq&q=j&li=20&l=false&jlo=en-US&j=software&jcoid=7c8c6665-81cf-4e11-8fc9-ec1d6a69120c&jl=37.09024%3A-95.71289100000001%3AUnited+States%3AUS%3AUS%3A1850.0791085354365%3ACOUNTRY%3A%3A%3A%3A%3A%3A&jld=20&',
            # 'https://careers.google.com/jobs#t=sq&q=j&li=20&st=20&l=false&jlo=en-US&j=software&jcoid=7c8c6665-81cf-4e11-8fc9-ec1d6a69120c&jl=37.09024%3A-95.71289100000001%3AUnited+States%3AUS%3AUS%3A1850.0791085354365%3ACOUNTRY%3A%3A%3A%3A%3A%3A&jld=20&',
            # 'https://careers.google.com/jobs#t=sq&q=j&li=20&st=40&l=false&jlo=en-US&j=software&jl=37.09024%3A-95.71289100000001%3AUnited+States%3AUS%3AUS%3A1850.0791085354365%3ACOUNTRY%3A%3A%3A%3A%3A%3A&jld=20&jcoid=7c8c6665-81cf-4e11-8fc9-ec1d6a69120c&',
            "https://careers.google.com/jobs#t=sq&q=j&li=20&l=false&jlo=en-US&jl=37.09024%3A-95.71289100000001%3AUnited+States%3AUS%3AUS%3A1850.0791085354365%3ACOUNTRY%3A%3A%3A%3A%3A%3A&jld=20&jdp=PAST_24_HOURS&"
        ]
        google_scraper = GoogleScraper()
        # input_file = "C:\\Users\Jon\Desktop\JobJolt\Code\JobJolt\JobBard\jobboard\scrape_tests/stackoverflow.xml"
        # print(input_file)
        # soScraper.openFile(input_file)
        # soScraper.scrape()

        for url in urls:
            print("Scraping: ", url)
            google_scraper.openUrl(url)
            google_scraper.scrape()
            time.sleep(15)
