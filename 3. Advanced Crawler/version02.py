"""
Master's Thesis - Web Scraping Implementation: Advanced Crawler - Version 2 (Playwright API Batch)

This script demonstrates a sophisticated approach to web scraping using Playwright's
APIRequestContext to process multiple backend API endpoints in a batch operation.
This version builds on Version 1 by implementing bulk data collection for 
greater efficiency and comprehensive product coverage.

Technical overview:
- Uses Playwright: A powerful browser automation library
- Uses APIRequestContext: Direct API access without browser rendering
- Batch processing: Retrieves data for multiple products sequentially
- Connection reuse: Maintains a single request context for efficiency
- Real-time status reporting: Provides feedback during execution
- Error handling: Gracefully manages failed requests without terminating
- JSON aggregation: Collects structured data into a unified result set

Advantages of batch API approach:
- Scales efficiently to handle multiple products
- Reuses connection for improved performance
- Preserves complete API response structure
- Provides real-time feedback on operation progress
- Maintains all benefits of direct API access from Version 1
- More efficient than individual script executions
- Fails gracefully when individual requests encounter errors

Limitations:
- Sequential processing may be slower than parallel requests
- No proxy implementation for IP rotation
- Vulnerable to rate limiting with larger product lists
- No retry mechanism for failed requests
- All requests use the same IP address, increasing detection risk
- Limited to a static, predefined list of product codes

Target URL: https://www.adidas.com/plp-app/api/product/{code}?sitePath=us
This endpoint pattern is used with multiple product codes to retrieve
comprehensive product information in JSON format for batch processing.
"""

import json  # For JSON serialization/deserialization
from typing import List, Dict  # Type annotations for improved code clarity
from playwright.sync_api import sync_playwright  # Playwright sync API for HTTP requests

# ──────────────────────────────────────────────────────────────────────────────
# List of Adidas product codes to fetch via the API
# These codes represent individual SKUs in Adidas's product catalog
# They typically follow a pattern of letters and numbers (e.g., "IH2265")
# This static list was extracted from pre-identified products of interest
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
    Fetch JSON data for each Adidas product code in batch mode.
    
    This function:
    1. Creates a single Playwright request context for connection efficiency
    2. Iterates through each product code in the provided list
    3. Constructs the appropriate API URL for each product
    4. Makes an HTTP GET request to the Adidas API for each product
    5. Collects successful responses into a result list
    6. Provides real-time feedback on each request's status
    
    The function maintains the complete JSON response structure, preserving
    all fields returned by the API for maximum data availability and
    flexibility in downstream processing.

    Args:
        codes (List[str]): List of product SKU codes to fetch.
                          Each code should be a valid Adidas product identifier.

    Returns:
        List[Dict]: List of parsed JSON objects, one per product.
                   Each dictionary contains the complete product information
                   as returned by the Adidas API.
    
    Error Handling:
        - Products that return non-200 status codes are logged but not included
          in the results list
        - The function continues processing remaining products even if some fail
    """
    # URL template for the Adidas product API
    # The {code} placeholder will be replaced with each individual product code
    # The sitePath parameter specifies the regional version of the site (us = United States)
    url_template: str = "https://www.adidas.com/plp-app/api/product/{code}?sitePath=us"
    
    # Container for successful API responses
    results: List[Dict] = []

    # Initialize Playwright sync context for API requests
    # The 'with' statement ensures proper resource cleanup even if exceptions occur
    with sync_playwright() as playwright:
        # Create a single request context that will be reused for all requests
        # This is more efficient than creating a new context for each request
        # as it can potentially reuse connections and maintain cookies/state
        request_context = playwright.request.new_context()

        # Process each product code sequentially
        for code in codes:
            # Construct the specific URL for this product using string formatting
            api_url = url_template.format(code=code)
            
            # Provide real-time feedback about the current operation
            # The end=" " parameter prevents a newline, so status appears on same line
            print(f"Fetching {code}...", end=" ")

            # Make the GET request to the Adidas API
            # This is a blocking call that waits for the response to complete
            response = request_context.get(api_url)
            
            # Check if the request was successful (HTTP 200 OK)
            if response.status == 200:
                # Extract the JSON data from the response and add to our results
                # response.json() automatically parses the JSON string into a Python dict
                results.append(response.json())
                print("Success ✔")  # Visual indicator of success
            else:
                # Handle the error case with appropriate feedback
                # This could be due to product not found, rate limiting, server errors, etc.
                print(f"Failed ✖ (HTTP {response.status})")

        # Properly dispose of the request context to release resources
        # This closes any open connections and frees memory
        request_context.dispose()

    # Return the collected results for further processing
    return results


if __name__ == "__main__":
    # This conditional block ensures the code only runs when executed directly
    # (not when imported as a module)
    
    # Execute batch fetch and print results
    # This calls our main function and stores the returned data
    products = fetch_all_products(PRODUCT_CODES)
    
    # Pretty-print the list of product JSONs to the terminal
    # The indent=2 parameter formats the output with 2-space indentation
    # for improved readability of the nested JSON structure
    print(json.dumps(products, indent=2))