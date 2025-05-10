"""
Master's Thesis – Advanced Crawler Version 3 (Batch Mode + Field Filtering + Proxy Support)

This batch script fetches selected product details from the Adidas API,
avoiding HTTP/2 protocol issues, ignoring HTTPS certificate errors,
using a proxy server, and minimizing returned fields for concise output.

Architecture Overview:
--------------------
1. Environment Configuration: Loads proxy credentials from .env file
2. Proxy Setup: Parses and configures proxy settings with authentication
3. Product Fetching: Uses Playwright's request context with proxy routing
4. Data Processing: Extracts only essential fields from the API response
5. Output Generation: Writes processed records to a structured JSON file

Technical Advantages:
-------------------
- SSL Certificate Bypass: Prevents connection issues with potentially untrusted proxies
- Minimized Payload: Reduces memory usage and improves processing speed
- Browser Fingerprinting: Uses realistic headers to avoid detection
- Error Resilience: Continues processing despite individual request failures
- Proxy Integration: Enables distributed access patterns to avoid rate limiting

Workflow:
--------
1. Load proxy credentials from .env file.
2. Define static list of Adidas product codes to fetch.
3. For each code:
   a. Build product-detail API URL.
   b. Send GET request through proxy with HTTPS errors ignored.
   c. Extract only title, original price, sale price, on-sale flag, and in-stock flag.
4. Aggregate minimal records into a Python list.
5. Write results to an output JSON file.

Enhancements:
------------
- Ignoring expired SSL certificates to prevent fetch errors.
- Field filtering reduces payload size and focuses on key attributes.
- Proxy support with proper authentication and SSL handling.
"""

import json  # For working with JSON data formats
import os  # For accessing environment variables
from typing import List, Dict  # Type annotations for improved code clarity
from playwright.sync_api import sync_playwright  # For making HTTP requests
from dotenv import load_dotenv  # For loading environment variables from .env file

# Load environment variables from .env file
# This allows storing sensitive data like proxy credentials outside the source code
# The dotenv library automatically finds and loads variables from a .env file in the project directory
load_dotenv()

# Step 1: Get proxy details from environment
# Retrieve the proxy URL string from the environment variables
# Format expected: https://username:password@host:port
PROXY_URL = os.getenv('PROXIES')
if not PROXY_URL:
    print("Warning: No proxy configuration found in .env file")

# Parse proxy details
# This section converts the proxy URL string into a configuration dictionary
# that Playwright can use to route requests through the proxy
proxy_config = None
if PROXY_URL:
    # Extract username, password, host, and port from the proxy URL
    # Format: https://username:password@host:port
    parts = PROXY_URL.replace('https://', '').split('@')
    if len(parts) == 2:
        # Split into authentication part and server part
        auth, server = parts
        auth_parts = auth.split(':')
        if len(auth_parts) >= 2:
            username = auth_parts[0]
            # Handle the case where password might contain colons
            # This is important because some proxy passwords may include special characters
            password = ':'.join(auth_parts[1:]) if ':' in auth[len(username)+1:] else auth_parts[1]
            
            # Create the proxy configuration dictionary for Playwright
            # Note: Even if the original URL uses HTTPS, the proxy connection uses HTTP
            proxy_config = {
                "server": f"http://{server}",  # The proxy server address with protocol
                "username": username,          # Authentication username
                "password": password           # Authentication password
            }
            print(f"Proxy configured: {server} (authenticated)")
        else:
            print("Error parsing proxy credentials")
    else:
        print("Invalid proxy URL format")

# Step 2: List of product codes extracted from DevTools
# These codes represent unique identifiers for Adidas products
# They were likely extracted from the Adidas website using browser DevTools
PRODUCT_CODES: List[str] = [
    "ID8732", "GV6900", "GV6902", "ID8605", "IE3370",
    "IE3526", "IE3528", "IE3530", "IE3532", "IF0244",
    "IF0245", "IF0246", "IF0249", "IF0299", "IF0316",
    "IF0322", "IF3270", "IF6606", "IG5916", "IG8105",
    "IH0935", "IH2198", "IH2264", "IH2265", "IH2266",
    "IH2267", "IH2268", "IH2270", "IH3357", "IH3398",
    "IH5992", "IH8436", "IH8445", "IH8504", "IH8523",
    "IH8553", "IH9887", "IH9888", "IH9977", "JH6149",
    "JH6150", "JH6151", "JH6153", "JH6154", "JI0861",
    "JI3940", "JI3941",
]

# Output file for minimal JSON records
# This defines where the results will be saved
OUTPUT_FILE: str = "advanced_crawler_products.json"


def fetch_all_products(codes: List[str], proxy_settings=None) -> List[Dict]:
    """
    Fetches minimal product info for each code through a simplified context.
    
    This function implements the core data collection logic by:
    1. Setting up a Playwright request context with proxy and SSL settings
    2. Adding realistic browser headers to avoid detection
    3. Fetching each product's data from the Adidas API
    4. Extracting only the essential fields from each response
    5. Handling errors gracefully to ensure the process completes
    
    The function implements data extraction at the source, rather than
    fetching complete responses and filtering later, improving efficiency
    and reducing memory usage.

    Args:
        codes: List of Adidas product codes to fetch data for.
              Each code is a string identifier (e.g., "IH2265").
        
        proxy_settings: Optional dictionary containing proxy configuration.
                       Expected format:
                       {
                           "server": "http://host:port",
                           "username": "user",
                           "password": "pass"
                       }
                       If None, requests are made directly without a proxy.
    
    Returns:
        Filtered list of product dictionaries with selected fields:
        - code: The product identifier
        - title: Product name/title
        - original_price: Regular product price
        - sale_price: Discounted price if available
        - on_sale: Boolean flag indicating if product is discounted
        - in_stock: Boolean flag indicating if product is available
    
    Error Handling:
        - Handles HTTP errors by continuing to the next product
        - Catches and reports any exceptions without terminating execution
        - Products with errors are logged but not included in results
    """
    # API URL template for Adidas product data
    # The {code} placeholder will be replaced with each product code
    url_template: str = "https://www.adidas.com/plp-app/api/product/{code}?sitePath=us"
    results: List[Dict] = []

    # Initialize Playwright for making API requests
    with sync_playwright() as p:
        # Create context with proxy settings (if provided) and ignoring HTTPS errors
        # The ignore_https_errors option is crucial when working with proxies
        # as it prevents SSL certificate validation failures
        context_options = {"ignore_https_errors": True}
        if proxy_settings:
            context_options["proxy"] = proxy_settings
        
        # Create the request context with our configured options
        request_ctx = p.request.new_context(**context_options)

        # Add a user agent to appear more like a regular browser
        # This helps avoid detection by anti-bot systems
        # The headers mimic a modern Chrome browser on Windows
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Accept": "application/json",  # We're expecting JSON responses
            "Accept-Language": "en-US,en;q=0.9",  # Preferred language
        }

        # Process each product code in the list
        for code in codes:
            # Construct the full API URL for this specific product
            api_url = url_template.format(code=code)
            print(f"Fetching {code}...", end=" ")
            
            try:
                # Make the HTTP request with our configured headers
                # This sends the request through the proxy if one is configured
                response = request_ctx.get(api_url, headers=headers)
                
                if response.status == 200:
                    # Extract only the product data from the response
                    # The .get() method provides safe access with default values
                    # if the keys don't exist
                    product = response.json().get('product', {})
                    price_data = product.get('priceData', {})

                    # Create a filtered record with only the fields we need
                    # This reduces memory usage and simplifies later analysis
                    record = {
                        'code': code,  # Product identifier
                        'title': product.get('title'),  # Product name
                        'original_price': price_data.get('price'),  # Regular price
                        'sale_price': price_data.get('salePrice'),  # Discounted price
                        # Calculate if the product is on sale by comparing prices
                        'on_sale': (
                            price_data.get('salePrice') is not None
                            and price_data.get('salePrice') < price_data.get('price')
                        ),
                        # Invert the isSoldOut flag to get in_stock status
                        'in_stock': not price_data.get('isSoldOut', True),
                    }
                    # Add the filtered record to our results list
                    results.append(record)
                    print('✔')  # Visual indicator of success
                else:
                    # Handle unsuccessful HTTP responses
                    print(f'✖ HTTP {response.status}')
                    
            except Exception as e:
                # Catch and report any exceptions without crashing the script
                # This ensures one failed request doesn't stop the entire process
                print(f'✖ Error: {str(e)}')

        # Clean up request context to free resources
        # This properly closes connections and releases memory
        request_ctx.dispose()

    # Return the collected results for further processing
    return results


def main():
    """
    Main function that orchestrates the data collection process.
    
    This function:
    1. Determines whether to use proxy based on configuration
    2. Initiates the product data fetching process
    3. Reports on the number of products successfully retrieved
    4. Writes the final results to the output JSON file
    
    The function serves as the entry point and coordinator for the script's
    execution flow.
    """
    # Run with proxy if configured, otherwise run directly
    if proxy_config:
        print(f"Starting fetch with proxy...")
        products = fetch_all_products(PRODUCT_CODES, proxy_config)
    else:
        print("Starting fetch without proxy...")
        products = fetch_all_products(PRODUCT_CODES)
        
    # Report on the number of products successfully retrieved
    print(f"Retrieved {len(products)} product records.")

    # Write filtered results to disk as a JSON file
    # The ensure_ascii=False parameter preserves Unicode characters
    # The indent=2 parameter formats the JSON for readability
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(products, f, indent=2, ensure_ascii=False)

    # Confirm successful completion
    print(f"✅ Written filtered results to '{OUTPUT_FILE}'")


if __name__ == '__main__':
    # Script entry point - execute the main function
    main()