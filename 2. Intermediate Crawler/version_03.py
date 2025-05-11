"""
Master's Thesis - Web Scraping Implementation: Intermediate Crawler - Version 3 (Httpx + Selectolax + Data Extraction)

This script demonstrates a complete web scraping solution using Python's
httpx library for HTTP requests and Selectolax for HTML parsing, with
structured data extraction and JSON output. This version represents 
a production-ready implementation for e-commerce data extraction.

Technical overview:
- Uses httpx: A modern, async-capable HTTP client
- Uses Selectolax: A fast HTML parser based on the Modest engine
- Comprehensive header configuration: Mimics real browser requests
- Structured data extraction: Efficiently extracts specific product data
- JSON output: Formats and saves results for further analysis
- Helper functions: Implements robust error handling for extraction
- Memory-efficient parsing: Uses Selectolax's lightweight DOM representation

Advantages of httpx + Selectolax parsing approach:
- Up to 5x faster HTML parsing than BeautifulSoup
- Lower memory usage than traditional parsers
- More maintainable than regex-based extraction
- Cleaner CSS selector syntax compared to XPath
- Efficient extraction of only needed data points
- Structured output suitable for analysis or database import
- Simpler implementation than Scrapy for medium-complexity tasks

Limitations:
- Still vulnerable to sophisticated bot detection
- No built-in JavaScript rendering capability
- Requires manual updates if site structure changes
- Not optimized for large-scale distributed crawling
- Limited middleware ecosystem compared to Scrapy

Target URL: https://www.rei.com/c/backpacking-packs
This website contains information about backpacking products which is
extracted and structured into a clean JSON format.
"""

import httpx
from selectolax.parser import HTMLParser
import re  # Needed for regex-based price cleanup
import json

# 1) Target URL: the REI page listing backpacking packs
# This e-commerce page contains a grid of product cards with details
url = "https://www.rei.com/c/backpacking-packs"

# 2) HTTP headers: mimic a real desktop browser to reduce basic bot detection
# These comprehensive headers build upon Version 2's approach for avoiding detection
# Each header serves a specific purpose in making the request appear legitimate:
#    - User-Agent: identifies browser type/version
#    - Accept*: what content types we can handle
#    - Accept-Encoding: allows gzip/br compression
#    - Connection: keep-alive to reuse TCP connection where possible
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1"
}

# Helper function to safely extract text using a CSS selector
# This function adds error handling to prevent crashes when elements aren't found
# and provides a consistent interface for text extraction throughout the script
def extract_text(html, sel):
    """
    Safely extract text content from an HTML element using a CSS selector.
    
    Args:
        html: A Selectolax HTML node to search within
        sel: A CSS selector string to locate the target element
        
    Returns:
        String content of the element or None if not found
    """
    try:
        return html.css_first(sel).text()
    except AttributeError:
        return None  # Return None if selector is not found

# 3) Send the GET request; set a 30-second timeout to fail fast if the page is slow
# Using the enhanced headers from Version 2 ensures we receive a complete response
resp = httpx.get(url, headers=headers, timeout=30.0)

# 4) Parse the raw HTML response with Selectolax for fast DOM traversal
# Selectolax is significantly faster and more memory-efficient than BeautifulSoup
# for parsing large HTML documents, especially for e-commerce pages with many products
html = HTMLParser(resp.text)

# 5) Identify each product container by its unique CSS class (inspected via DevTools)
# This CSS selector targets the list item that contains each product card
# These selectors were determined by inspecting the page structure in browser developer tools
products = html.css("li.VcGDfKKy_dvNbxUqm29K")

all_items = []
# 6) Loop through each product element and pull out the fields we care about
# This structured approach extracts only the specific data needed, rather than
# processing the entire HTML document, making it more efficient
for product in products:
    # Create a dictionary for each product with extracted data
    # The extract_text helper ensures consistent error handling
    item = {
        "name": extract_text(product, ".Xpx0MUGhB7jSm5UvK2EY"),
        "full_price": extract_text(product, "span[data-ui=full-price]"),
        "sale_price": extract_text(product, "span[data-ui=sale-price]")
    }

    # Add the completed item to our results list
    all_items.append(item)

# 7) Write the results to a JSON file for easy import into other tools or inclusion
# JSON is a versatile format that can be easily used in data analysis or loaded into databases
output_file = "intermediate_crawler_products.json"
with open(output_file, "w", encoding="utf-8") as f:
    # ensure_ascii=False preserves non-ASCII characters like currency symbols
    # indent=2 makes the output file human-readable
    json.dump(all_items, f, ensure_ascii=False, indent=2)

# 8) Print a confirmation so you know how many items were scraped and where to find them
# This provides immediate feedback on the success of the scraping operation
print(f"✅ Scraped {len(all_items)} products → {output_file}")

# Note: For production use, this script could be enhanced with:
# - Proxy rotation to distribute requests across different IP addresses
# - Rate limiting to avoid triggering anti-bot measures
# - Retry logic for handling temporary failures
# - More extensive error handling and logging
# - Incremental scraping to handle pagination
# These advanced features will be explored in the Advanced crawler implementation.