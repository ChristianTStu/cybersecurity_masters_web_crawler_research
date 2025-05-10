"""
Master's Thesis – Advanced Crawler Version 1.1 (Batch Mode)

This script fetches JSON product details in bulk from the Adidas API.
It uses Playwright's APIRequestContext for direct HTTP calls, avoiding browser navigation
and mitigating HTTP/2 protocol issues.

Workflow:
1. Define a static list of Adidas product codes (e.g., 'IE3530').
2. Construct the product-detail API URL for each code and fetch its JSON payload.
3. Collect all product JSON objects into a single Python list.
4. Print the aggregated list to the terminal.

Future Enhancements:
- Add proxy rotation for distributed requests.
- Integrate CAPTCHA solving when anti-bot measures are encountered.
- Introduce retries with exponential backoff for transient failures.
"""

import json
from typing import List, Dict
from playwright.sync_api import sync_playwright  # Playwright sync API for HTTP requests

# ──────────────────────────────────────────────────────────────────────────────
# List of Adidas product codes to fetch via the API
PRODUCT_CODES: List[str] = [
    "ID8732", "GV6900", "GV6902", "ID8605", "IE3370", "IE3526", "IE3528",
    "IE3530", "IE3532", "IF0244", "IF0245", "IF0246", "IF0249", "IF0299",
    "IF0316", "IF0322", "IF3270", "IF6606", "IG5916", "IG8105", "IH0935",
    "IH2198", "IH2264", "IH2265", "IH2266", "IH2267", "IH2268", "IH2270",
    "IH3357", "IH3398", "IH5992", "IH8436", "IH8445", "IH8504", "IH8523",
    "IH8553", "IH9887", "IH9888", "IH9977", "JH6149", "JH6150", "JH6151",
    "JH6153", "JH6154", "JI0861", "JI3940", "JI3941",
]
# ──────────────────────────────────────────────────────────────────────────────

def fetch_all_products(codes: List[str]) -> List[Dict]:
    """
    Fetch JSON data for each Adidas product code.

    Args:
        codes (List[str]): List of product SKU codes to fetch.

    Returns:
        List[Dict]: List of parsed JSON objects, one per product.
    """
    url_template: str = "https://www.adidas.com/plp-app/api/product/{code}?sitePath=us"
    results: List[Dict] = []

    # Initialize Playwright sync context for API requests
    with sync_playwright() as playwright:
        request_context = playwright.request.new_context()

        for code in codes:
            api_url = url_template.format(code=code)
            print(f"Fetching {code}...", end=" ")

            response = request_context.get(api_url)
            if response.status == 200:
                results.append(response.json())
                print("Success ✔")
            else:
                print(f"Failed ✖ (HTTP {response.status})")

        request_context.dispose()

    return results


if __name__ == "__main__":
    # Execute batch fetch and print results
    products = fetch_all_products(PRODUCT_CODES)
    # Pretty-print the list of product JSONs to the terminal
    print(json.dumps(products, indent=2))
