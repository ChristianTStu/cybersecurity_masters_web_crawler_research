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

Technical Architecture:
---------------------
1. Setup Playwright synchronous context
2. Create API request context
3. Send GET request to Adidas product API
4. Process and display JSON response
5. Clean up resources

Benefits:
--------
- Lighter weight than full browser automation
- Avoids HTTP/2 protocol complexities
- Direct JSON access without HTML parsing
- More efficient for batch processing
"""

from playwright.sync_api import sync_playwright  # Import the synchronous Playwright API
import json  # Import the JSON module for processing API responses

def fetch_adidas_product():
    """
    Fetches product data from the Adidas API for a specific product ID.
    
    This function:
    1. Establishes a connection to the Adidas product API
    2. Retrieves raw JSON data for the specified product
    3. Processes and displays the complete product information
    
    No parameters are required as the product ID is hardcoded for demonstration.
    
    Returns:
        None - Results are printed to console
    """
    # Target API endpoint for product JI0861 on the US site
    # The URL follows Adidas's API structure: base/api/product/{product_id}?sitePath={region}
    # This endpoint returns comprehensive product information including pricing, availability, and specs
    url = "https://www.adidas.com/plp-app/api/product/JI0861?sitePath=us"

    # Initialize Playwright for synchronous API requests
    # The 'with' statement ensures proper resource management and cleanup
    with sync_playwright() as p:
        # Create an isolated request context for API calls
        # This context manages headers, cookies, and connection settings
        # Unlike browser context, this is lightweight and optimized for API interactions
        request_context = p.request.new_context()

        # Send a GET request to the API endpoint
        # This makes an HTTP GET request to retrieve the product data
        # The method handles connection establishment, request headers, and response parsing
        response = request_context.get(url)
        
        # Check if the request was successful (HTTP 200 OK)
        # Status codes other than 200 indicate error conditions like:
        # - 404: Product not found
        # - 403: Access forbidden (possible rate limiting)
        # - 500: Server error
        if response.status != 200:
            print(f"❌ Failed to fetch data (status {response.status}).")
        else:
            # Parse the response body as JSON
            # This converts the raw response text into a structured Python dictionary
            data = response.json()
            
            # Pretty-print the JSON data with indentation for readability
            # The indent=2 parameter formats the output with 2-space indentation
            # This makes the complex nested structure more human-readable
            print(json.dumps(data, indent=2))

        # Dispose of the request context to free up resources
        # This explicitly releases network connections and memory
        # Important for efficiency in scripts that run many requests
        request_context.dispose()

if __name__ == "__main__":
    # Entry point: execute the fetch function
    # This conditional ensures the function only runs when the script is executed directly
    # (not when imported as a module into another script)
    fetch_adidas_product()