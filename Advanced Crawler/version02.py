"""
Master's Thesis – Advanced Crawler Version 2 (Batch Mode)

This script fetches JSON product details in bulk from the Adidas API.
It uses Playwright's APIRequestContext for direct HTTP calls, avoiding browser navigation
and mitigating HTTP/2 protocol issues.

Workflow:
1. Define a static list of Adidas product codes (e.g., 'IE3530').
2. Construct the product-detail API URL for each code and fetch its JSON payload.
3. Collect all product JSON objects into a single Python list.
4. Print the aggregated list to the terminal.

Technical Implementation Details:
--------------------------------
- Uses a single APIRequestContext to maintain connection efficiency
- Implements sequential fetching with real-time status reporting
- Handles HTTP response status codes to identify successful vs. failed requests
- Preserves the complete API response structure for maximum data availability

Design Principles:
-----------------
- Separation of concerns: Data collection separated from data processing
- Fail gracefully: Continue processing despite individual request failures
- Transparency: Real-time feedback on request status
- Efficiency: Direct API access without browser overhead

Future Enhancements:
-------------------
- Add proxy rotation for distributed requests.
- Integrate CAPTCHA solving when anti-bot measures are encountered.
- Introduce retries with exponential backoff for transient failures.
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