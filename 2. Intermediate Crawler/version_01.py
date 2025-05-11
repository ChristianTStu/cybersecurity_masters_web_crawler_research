"""
Master's Thesis - Web Scraping Implementation: Intermediate Crawler - Version 1 (Httpx + Selectolax)

This script demonstrates a basic approach to web scraping using Python's
httpx library for HTTP requests and Selectolax for HTML parsing. This version
intentionally encounters challenges with sophisticated anti-bot systems to
highlight the limitations of simple scraping approaches.

Technical overview:
- Uses httpx: A modern, async-capable HTTP client
- Uses Selectolax: A fast HTML parser based on the Modest engine
- Simple request structure: Basic header configuration
- Minimal error handling: Shows raw failure modes
- Demonstrates anti-bot protection in action: Request times out or fails

Advantages of httpx + Selectolax approach:
- Supports both synchronous and asynchronous requests
- Better HTTP/2 support than requests
- More modern API design than urllib
- Selectolax offers faster parsing than BeautifulSoup
- Lower memory usage than traditional parsers
- Simple installation and minimal dependencies

Limitations:
- Insufficient for sites with sophisticated bot detection
- No built-in JavaScript rendering capability
- Simple headers easily detected as non-browser traffic
- Cannot bypass most modern anti-scraping technologies
- No session or cookie management in this basic implementation

Target URL: https://www.rei.com/c/backpacking-packs
This website contains information about backpacking products which will be
attempted to be extracted in different ways across the three versions of the scraper.
"""

import httpx
from selectolax.parser import HTMLParser

# The target URL to be scraped
# An e-commerce page with product listings for backpacking packs
url = "https://www.rei.com/c/backpacking-packs"

# Basic header configuration with a simple User-Agent
# This minimal approach is intentionally insufficient for modern websites
# with anti-bot protection, demonstrating the need for more sophisticated techniques
headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"}

# Attempt to make a GET request to the target URL
# The timeout parameter is set to 30 seconds to allow for slower responses
# However, this request is expected to fail or time out due to anti-bot measures
#
# Under the hood, this:
# 1. Establishes an HTTP connection to the server
# 2. Sends the GET request with minimal headers
# 3. Waits for a response that likely won't arrive properly
# 4. Eventually times out or receives a blocking response
resp = httpx.get(url, headers=headers, timeout=30.0)

# Print the HTTP status code of the response
# Expected outcome: Either a timeout exception or a 403 Forbidden response
# This demonstrates that simple requests are insufficient for complex commercial sites
print(resp.status_code)

# Note: The script intentionally does not implement error handling or
# parse the HTML response, as the request is expected to fail.
# This illustrates the need for more sophisticated approaches in Version 2 and 3.