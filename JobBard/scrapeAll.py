import os
import random
import sys


def main():
    commands = [
        'scrapeApple',
        'scrapeAmazon',
        'scrapeGithub',
        'scrapeGoogle',
        'scrapeGreenhouse',
        'scrapeLever',
        'scrapeMicrosoft',
        'scrapeSalesforce',
        'scrapeStackoveflow',
        'scrapeTwitter',
        'scrapeIBM'

    ]
    random.shuffle(commands)
    for arg in commands:
        sys.argv = [arg]
        print(arg, '...')
        os.system('manage.py ' + arg)


if __name__ == '__main__':
    main()
