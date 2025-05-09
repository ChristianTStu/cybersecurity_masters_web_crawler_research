"""
Summary:
--------
This script uses Playwright's APIRequestContext to fetch JSON data for a product from the Adidas API.
It avoids HTTP/2 protocol errors by using direct request context instead of navigating a browser page.

Version:
--------
Advanced Crawler Version 01 for Master's Thesis demonstration.

Note:
-----
- This is the introductory version focusing on simple API retrieval without browser automation.
- Later versions will build on this by adding proxy support and possibly CAPTCHA solving.
"""

from playwright.sync_api import sync_playwright
import json

def fetch_adidas_product():
    # Target API endpoint for product JI0861 on the US site
    url = "https://www.adidas.com/plp-app/api/product/JI0861?sitePath=us"

    # Initialize Playwright for synchronous API requests
    with sync_playwright() as p:
        # Create an isolated request context for API calls
        request_context = p.request.new_context()

        # Send a GET request to the API endpoint
        response = request_context.get(url)
        
        # Check if the request was successful (HTTP 200 OK)
        if response.status != 200:
            print(f"❌ Failed to fetch data (status {response.status}).")
        else:
            # Parse the response body as JSON
            data = response.json()
            # Pretty-print the JSON data with indentation for readability
            print(json.dumps(data, indent=2))

        # Dispose of the request context to free up resources
        request_context.dispose()

if __name__ == "__main__":
    # Entry point: execute the fetch function
    fetch_adidas_product()