# JobBard
A personal tool for scraping jobs from various tech-centered job sites.

## What is JobBard?
  JobBard is a simple and ongoing tool geared toward finding users a software engingeering job. It works by scraping various tech-centered companies from across the web for job postings. While still a work in progress, JobBard aims to not only give software developers a list of up-to-date jobs but give them a simple web interface to track their application progress with multiple companies at once.
  
## How can I scrape sites that aren't yet added?
  JobBard provides some base classes to make scraping jobs from potentially any source. Create a new python class derived from one of the three base classes below and define the scrape pattern as well as any function overrides to obtain the required data. JobBard uses BeautifulSoup4 to narrow down HTML until we want. The scrape_pattern variable and overriden fucntions are intended to tailor where specifically the data is on the page- for example a job title may be surronded by <div> tags with a certain class, id, attribute. 
  
  The base classes are:
  ## AbstractJobScraper
    Used to scrape static HTML.
  ## JsonScraper
    Used to scrape jobs in JSON format, typically from public APIs.
  ## RenderedScraper
    Derived from the AbstractJobScraper, the RenderedScraper uses Selenium in order to scrape pages that dynamically load content via javascript.
    The RenderedScraper also allows for custom javascript to be executed in the page- for example to fill out search fields in a job search page.
