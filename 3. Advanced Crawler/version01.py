"""
Master's Thesis - Web Scraping Implementation: Advanced Crawler - Version 1 (Playwright API Direct)

This script demonstrates a sophisticated approach to web scraping using Playwright's
APIRequestContext to directly access backend API endpoints rather than scraping HTML.
This version represents a modern implementation targeting structured data sources
with minimal overhead and maximum efficiency.

Technical overview:
- Uses Playwright: A powerful browser automation library
- Uses APIRequestContext: Direct API access without browser rendering
- Single endpoint access: Retrieves data for one specific product
- JSON processing: Works with structured data instead of HTML
- Resource management: Properly initializes and disposes of contexts

Advantages of Playwright API approach:
- Bypasses frontend rendering completely
- Avoids complex HTML parsing and CSS selectors
- Receives data in structured JSON format
- Lower resource usage than full browser automation
- Avoids bot detection mechanisms tied to browser fingerprinting
- More stable than scraping dynamically rendered content
- Direct access to the same data sources used by the website

Limitations:
- Requires discovering and understanding API endpoints
- API structure may change without notice
- Single product focus lacks scalability
- No proxy implementation for IP rotation
- Potentially vulnerable to API rate limiting
- Requires manual inspection to discover API patterns

Target URL: https://www.adidas.com/plp-app/api/product/JI0861?sitePath=us
This endpoint provides comprehensive product information in JSON format,
demonstrating how to access backend APIs directly instead of scraping HTML.
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