"""
This script performs an HTTP GET request to the REI backpacking packs category page,
using the httpx library with an expanded set of HTTP headers to better mimic a real browser request.

The additional headers help increase the likelihood of receiving a full 200 OK response
and the complete HTML content of the page, bypassing basic bot detection mechanisms.

While this approach successfully retrieves the full HTML markup, parsing such large raw content 
can become cumbersome. Therefore, the next development step will focus on implementing logic 
to extract only relevant data — specifically, product pricing and associated item details.
"""

import httpx
from selectolax.parser import HTMLParser

url = "https://www.rei.com/c/backpacking-packs"

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

resp = httpx.get(url, headers=headers, timeout=30.0)

print(resp.status_code)
print(resp.text)


