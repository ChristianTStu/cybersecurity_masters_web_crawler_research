"""
Version 1: Basic HTTPx + Selectolax Scraper
------------------------------------------
PURPOSE:
  • Demonstrate a naïve, “out-of-the-box” scraping approach against Napaonline
  • No browser emulation, stealth, proxies, or CAPTCHA handling—expected to be blocked

USAGE:
  Run this script as-is. You should see an empty list (`[]`) or a “403 Forbidden Error,”
  illustrating that simple HTTP requests cannot bypass Napaonline’s protections,
  necessitating a more advanced approach.
"""


import httpx
from selectolax.parser import HTMLParser
import re

# ─── Configuration ─────────────────────────────────────────────────────────────

# 1) Target category page URL
CATEGORY_URL  = (
    "https://www.napaonline.com/en/shop/"
    "replacement-parts/batteries/automotive-batteries/car-batteries/315705233"
)

# 2) CSS selector for each product tile (container)
CONTAINER_SEL = "geo-product-list-item"

# 3) Within each tile, the selector for the product title/details
TITLE_SEL     = "div.geo-pod-detail"

# 4) Within each tile, the selector for the displayed price
PRICE_SEL     = "div.geo-plp-product_base_price"

# ─── Helper Function ────────────────────────────────────────────────────────────

def extract_text(node, selector):
    """
    Safely extract text from the first matching CSS selector under `node`.
    Returns None if the selector isn’t found or in case of any error.
    """
    try:
        return node.css_first(selector).text().strip()
    except:
        return None

# ─── Main Scrape Logic ──────────────────────────────────────────────────────────

def run_basic():
    # 1. Send a plain HTTP GET request
    resp = httpx.get(CATEGORY_URL, timeout=30.0)
    resp.raise_for_status()

    # 2. Parse the response HTML with Selectolax
    tree = HTMLParser(resp.text)

    # 3. Find all product containers
    cards = tree.css(CONTAINER_SEL)

    # 4. Extract name & price from each container
    results = []
    for card in cards:
        name      = extract_text(card, TITLE_SEL)
        raw_price = extract_text(card, PRICE_SEL)
        price     = re.sub(r"[^\d\.]", "", raw_price) if raw_price else None

        results.append({
            "name":  name,
            "price": price
        })

    # 5. Print what we found (likely an empty list)
    print(results)

# ─── Entry Point ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    run_basic()
