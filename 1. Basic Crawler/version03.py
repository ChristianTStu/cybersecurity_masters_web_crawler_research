"""
Master's Thesis - Web Scraping Implementation: Advanced Crawler - Version 3 (Scrapy + BeautifulSoup)

This script demonstrates an advanced approach to web scraping using Python's
Scrapy framework combined with BeautifulSoup for HTML parsing. This version
represents a production-grade implementation with structured data extraction,
asynchronous processing, and output formatting.

Technical overview:
- Uses Scrapy: A comprehensive web crawling framework
- Uses BeautifulSoup: A powerful HTML parsing library
- Asynchronous architecture: Handles concurrent requests efficiently
- Structured data extraction: Parses HTML and extracts specific data points
- Automatic output formatting: Exports data to JSON file
- Advanced configuration: Controls logging, output, and crawler behavior

Advantages of Scrapy + BeautifulSoup approach:
- High performance with asynchronous processing
- Built-in support for distributed crawling
- Comprehensive middleware system for request/response processing
- Robust handling of malformed HTML with BeautifulSoup
- Extensible pipeline for data processing
- Simple data export to various formats (JSON, CSV, XML, etc.)
- Production-ready with configurable policies for crawling behavior

Limitations:
- Steeper learning curve compared to simpler approaches
- More dependencies to manage
- Potentially excessive for very simple scraping tasks
- Requires understanding of the Scrapy architecture

Target URL: https://www.scrapethissite.com/pages/simple/
This website contains information about countries which is extracted
and structured into a clean JSON format.
"""

import json
from scrapy import Spider
from scrapy.crawler import CrawlerProcess
from bs4 import BeautifulSoup


class SimpleSpider(Spider):
    """
    Scrapy Spider class that defines how to crawl and parse the target website.
    
    This class:
    1. Defines the starting URL(s) to crawl
    2. Implements a parse method that processes each HTTP response
    3. Uses BeautifulSoup to navigate the HTML DOM structure
    4. Extracts structured data about countries
    5. Yields the extracted data for further processing/storage
    
    The Spider class is a core component of the Scrapy framework,
    providing a systematic way to define crawling behavior.
    """
    name = 'simple_spider'  # Name of the spider, used by Scrapy internally
    start_urls = ['https://www.scrapethissite.com/pages/simple/']  # URLs to begin crawling

    def parse(self, response):
        """
        Parse the HTML with BeautifulSoup, extracting country name, capital, and population.
        
        This method is automatically called by Scrapy for each of the start_urls.
        It represents the main logic for processing the fetched HTML content
        and extracting structured data.
        
        Args:
            response: A Scrapy Response object containing the page content
                      and metadata about the HTTP response
        
        Yields:
            dict: A dictionary containing extracted country data with keys:
                  'country', 'capital', and 'population'
        """
        # Create a BeautifulSoup object for HTML parsing
        # The 'html.parser' is Python's built-in HTML parser
        # BeautifulSoup provides powerful methods to navigate and search the HTML DOM
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Each country is within a <div class="country"> container
        # The select() method finds all elements matching the CSS selector
        for container in soup.select('div.country'):
            # Country name is in an h3 element with class 'country-name'
            # select_one() returns the first matching element or None
            name_el = container.select_one('h3.country-name')
            
            # Info block containing capital and population
            # This div contains multiple spans with country details
            info = container.select_one('div.country-info')
            
            # Skip this container if either essential element is missing
            if not name_el or not info:
                continue

            # Extract the country name, stripping whitespace
            country_name = name_el.get_text(strip=True)
            
            # Extract capital city name from its span element
            capital_el = info.select_one('span.country-capital')
            capital = capital_el.get_text(strip=True) if capital_el else None
            
            # Extract population and convert to integer if possible
            # This demonstrates type conversion for numeric data
            pop_el = info.select_one('span.country-population')
            population = None
            if pop_el:
                # Remove commas from numbers (e.g., "1,234,567" -> "1234567")
                pop_text = pop_el.get_text(strip=True).replace(',', '')
                try:
                    # Convert string to integer
                    population = int(pop_text)
                except ValueError:
                    # Handle cases where conversion fails
                    population = None

            # Yield the extracted data as a dictionary
            # Scrapy will collect these results and process them according
            # to the configured output settings (in this case, JSON output)
            yield {
                'country': country_name,
                'capital': capital,
                'population': population
            }


if __name__ == '__main__':
    # Configure and run the Scrapy spider, outputting to JSON
    # CrawlerProcess is Scrapy's main entry point for running spiders
    # from a script rather than from the command line
    process = CrawlerProcess({
        # Configure the output format as JSON
        'FEED_FORMAT': 'json',
        # Specify the output file path
        'FEED_URI': 'basic_crawler_products.json',
        # Set logging level to ERROR to reduce console output
        # Other options include DEBUG, INFO, WARNING, ERROR, CRITICAL
        'LOG_LEVEL': 'ERROR'
    })
    
    # Register our spider with the crawler process
    process.crawl(SimpleSpider)
    
    # Start the crawling process - this is a blocking call
    # that will run until all spiders are finished
    process.start()
    
    # Notify the user that the process is complete
    print('✅ Data written to basic_crawler_products.json')