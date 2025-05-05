"""
This script attempts to perform an HTTP GET request to the REI backpacking packs category page
using the httpx library and a basic User-Agent header.

However, due to the site's use of advanced bot detection and protection mechanisms 
(such as Akamai, Cloudflare, or Datadome), the request fails to return even a valid HTTP status code. 
Instead, the connection is stalled or silently blocked, ultimately causing a read timeout.

This highlights the limitations of using simple HTTP clients like httpx when accessing 
heavily protected or JavaScript-driven websites, where a headless browser or more advanced 
scraping approach is required to bypass these defenses.
"""

import httpx
from selectolax.parser import HTMLParser

url = "https://www.rei.com/c/backpacking-packs"

headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"}

resp = httpx.get(url, headers=headers, timeout=30.0)
print(resp.status_code)
