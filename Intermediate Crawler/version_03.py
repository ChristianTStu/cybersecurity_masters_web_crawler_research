"""
intermediate_playwright_crawler.py
----------------------------------
This script scrapes product names and prices from the REI backpacking packs category page
and saves the results to a JSON file for later analysis or inclusion in your thesis.

Key steps:
1. Define the target URL and HTTP headers to mimic a real browser.
2. Send an HTTP GET request using httpx with a timeout to avoid hanging.
3. Parse the returned HTML using Selectolax for fast, memory-efficient parsing.
4. Locate each product container via CSS selectors (inspected in Chrome DevTools).
5. Extract the product name, full price, and sale price for each item.
6. Store all extracted items in a list of dicts.
7. Write the list to a JSON file with indentation for readability.
8. Print a summary of how many items were scraped and where the file was saved.

Note on anti-bot protections:
REI may throttle or block rapid or repeated requests. In a production consider adding randomized delays, proxy rotation, or switching to
a headless browser approach (e.g., Playwright) for greater resilience. Thus will be explored in the Advanced crawler.
"""

import httpx
from selectolax.parser import HTMLParser
import re  # Needed for regex-based price cleanup
import json

# 1) Target URL: the REI page listing backpacking packs
url = "https://www.rei.com/c/backpacking-packs"

# 2) HTTP headers: mimic a real desktop browser to reduce basic bot detection
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
def extract_text(html, sel):
    try:
        return html.css_first(sel).text()
    except AttributeError:
        return None  # Return None if selector is not found

# 3) Send the GET request; set a 30-second timeout to fail fast if the page is slow
resp = httpx.get(url, headers=headers, timeout=30.0)

# 4) Parse the raw HTML response with Selectolax for fast DOM traversal
html = HTMLParser(resp.text)

# 5) Identify each product container by its unique CSS class (inspected via DevTools)
# (found using Chrome DevTools to inspect the REI site)
products = html.css("li.VcGDfKKy_dvNbxUqm29K")

all_items = []
# 6) Loop through each product element and pull out the fields we care about
for product in products:
    item = {
        "name": extract_text(product, ".Xpx0MUGhB7jSm5UvK2EY"),
        "full_price": extract_text(product, "span[data-ui=full-price]"),
        "sale_price": extract_text(product, "span[data-ui=sale-price]")
    }

    all_items.append(item)

# 7) Write the results to a JSON file for easy import into other tools or inclusion
output_file = "intermediate_crawler_products.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(all_items, f, ensure_ascii=False, indent=2)

# 8) Print a confirmation so you know how many items were scraped and where to find them
print(f"✅ Scraped {len(all_items)} products → {output_file}")