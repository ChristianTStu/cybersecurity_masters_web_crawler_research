# version03_scrapy_bs.py
# Version 3: Scrapy + BeautifulSoup
# Parses the Simple page and outputs structured JSON containing country name, capital, and population.

import json
from scrapy import Spider
from scrapy.crawler import CrawlerProcess
from bs4 import BeautifulSoup

class SimpleSpider(Spider):
    name = 'simple_spider'
    start_urls = ['https://www.scrapethissite.com/pages/simple/']

    def parse(self, response):
        """
        Parse the HTML with BeautifulSoup, extracting country name, capital, and population.
        """
        soup = BeautifulSoup(response.text, 'html.parser')
        # Each country is within a <div class="country"> container
        for container in soup.select('div.country'):
            # Country name
            name_el = container.select_one('h3.country-name')
            # Info block containing capital and population
            info = container.select_one('div.country-info')
            if not name_el or not info:
                continue

            country_name = name_el.get_text(strip=True)
            # Extract capital
            capital_el = info.select_one('span.country-capital')
            capital = capital_el.get_text(strip=True) if capital_el else None
            # Extract population and convert to int if possible
            pop_el = info.select_one('span.country-population')
            population = None
            if pop_el:
                pop_text = pop_el.get_text(strip=True).replace(',', '')
                try:
                    population = int(pop_text)
                except ValueError:
                    population = None

            yield {
                'country': country_name,
                'capital': capital,
                'population': population
            }

if __name__ == '__main__':
    # Configure and run the Scrapy spider, outputting to JSON
    process = CrawlerProcess({
        'FEED_FORMAT': 'json',
        'FEED_URI': 'simple_countries.json',
        'LOG_LEVEL': 'ERROR'
    })
    process.crawl(SimpleSpider)
    process.start()  # blocking call
    print('✅ Data written to simple_countries.json')
