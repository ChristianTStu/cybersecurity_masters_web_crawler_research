"""
Master's Thesis - Web Scraping Implementation: Intermediate Crawler - Version 2 (Httpx + Enhanced Headers)

This script demonstrates an improved approach to web scraping using Python's
httpx library with enhanced request headers to bypass basic anti-bot detection.
This version successfully retrieves the full HTML content by better mimicking
legitimate browser behavior.

Technical overview:
- Uses httpx: A modern, async-capable HTTP client
- Comprehensive header configuration: Mimics real browser requests
- Successful response handling: Retrieves complete HTML content
- Minimal parsing: Demonstrates successful retrieval without data extraction
- Bypasses basic protection: Overcomes simple anti-bot mechanisms

Advantages of enhanced headers approach:
- Successfully bypasses basic anti-bot detection
- Maintains the speed and efficiency of httpx
- No additional dependencies required beyond Version 1
- Demonstrates a common and effective scraping technique
- Preserves the option for async implementation
- More reliable than basic requests

Limitations:
- Still vulnerable to sophisticated bot detection
- Returns excessive data without structured extraction
- Memory intensive when dealing with large HTML pages
- No JavaScript rendering capability
- Manual header maintenance as browser fingerprints evolve

Target URL: https://www.rei.com/c/backpacking-packs
This website contains information about backpacking products which will be
retrieved successfully but not yet structured into usable data.
"""

import httpx
from selectolax.parser import HTMLParser

# The target URL to be scraped
# An e-commerce page with product listings for backpacking packs
url = "https://www.rei.com/c/backpacking-packs"

# Enhanced header configuration to mimic a real browser
# These additional headers help bypass basic anti-bot detection by:
# 1. Providing a complete and current User-Agent string
# 2. Including expected Accept headers for content types
# 3. Adding language preferences typical of real browsers
# 4. Setting proper encoding options
# 5. Including modern security-related fetch metadata
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

# Make a GET request to the target URL with enhanced headers
# Unlike Version 1, this request is expected to succeed because:
# - The comprehensive headers make the request appear more legitimate
# - Basic anti-bot mechanisms are bypassed with this approach
#
# Under the hood, this:
# 1. Establishes an HTTP connection to the server
# 2. Sends the GET request with comprehensive browser-like headers
# 3. Waits for the server response
# 4. Receives and processes the HTTP response
resp = httpx.get(url, headers=headers, timeout=30.0)

# Print the HTTP status code of the response
# Expected outcome: 200 OK, indicating successful retrieval
# This demonstrates the effectiveness of proper header configuration
print(resp.status_code)

# Print the full HTML content of the page
# This demonstrates successful retrieval but shows the need for
# targeted extraction in Version 3 as the raw HTML is voluminous
# and difficult to work with directly
print(resp.text)

# Note: While this script successfully retrieves the HTML,
# it does not yet implement structured data extraction.
# Version 3 will address this limitation by adding parsing
# logic to extract specific product information.

