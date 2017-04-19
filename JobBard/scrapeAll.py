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
        'scrapeStackoverflow',
        'scrapeTwitter',
        'scrapeIBM',
        'scrapeCisco',
        'scrapeFacebook',

    ]
    random.shuffle(commands)
    commands.append('printTodayStats')
    for arg in commands:
        sys.argv = [arg]
        print(arg, '...')
        os.system('manage.py ' + arg)


if __name__ == '__main__':
    main()
