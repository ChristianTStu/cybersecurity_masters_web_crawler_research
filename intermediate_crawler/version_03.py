"""
Summary:
--------
This script scrapes product names and sale prices from the REI backpacking packs category page.
It uses the httpx library to send an HTTP GET request with detailed browser-mimicking headers,
and Selectolax to parse the returned HTML.

The script identifies individual product blocks using CSS selectors (located via Chrome DevTools),
extracts product names and sale prices, and cleans up the price strings by removing 
any additional discount or comparison text.

Note:
------
Due to REI's anti-bot protections, repeated or fast scraping may lead to temporary IP blocks.
It’s recommended to run this script cautiously with delays or consider upgrading to 
a headless browser solution like Playwright for more robust scraping.
"""

import httpx
from selectolax.parser import HTMLParser
import re  # Needed for regex-based price cleanup

# Define the target URL for backpacking packs
url = "https://www.rei.com/c/backpacking-packs"

# Define headers to mimic a real browser request and avoid basic bot detection
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
def extract_text(html, sel):
    try:
        return html.css_first(sel).text()
    except AttributeError:
        return None  # Return None if selector is not found

# Send the HTTP GET request with a 30-second timeout
resp = httpx.get(url, headers=headers, timeout=30.0)

# Parse the raw HTML response using Selectolax
html = HTMLParser(resp.text)

# Identify product containers on the page using the known CSS class
# (found using Chrome DevTools to inspect the REI site)
products = html.css("li.VcGDfKKy_dvNbxUqm29K")

# Loop over each product block and extract relevant details
for product in products:
    raw_price = extract_text(product, "span[data-ui=sale]")

    if raw_price:
        # Clean up the price string by removing trailing discount or comparison text
        clean_price = re.split(r'Save|compared', raw_price)[0].strip()
    else:
        clean_price = None

    # Build the item dictionary with product name and cleaned price
    item = {
        "name": extract_text(product, ".Xpx0MUGhB7jSm5UvK2EY"),
        "price": clean_price,
    }

    # Print the extracted product details
    print(item)
