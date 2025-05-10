"""
Master's Thesis – Advanced Crawler Version 3 (Batch Mode + Field Filtering + Proxy Support)

This batch script fetches selected product details from the Adidas API,
avoiding HTTP/2 protocol issues, ignoring HTTPS certificate errors,
using a proxy server, and minimizing returned fields for concise output.

Workflow:
1. Load proxy credentials from .env file.
2. Define static list of Adidas product codes to fetch.
3. For each code:
   a. Build product-detail API URL.
   b. Send GET request through proxy with HTTPS errors ignored.
   c. Extract only title, original price, sale price, on-sale flag, and in-stock flag.
4. Aggregate minimal records into a Python list.
5. Write results to an output JSON file.

Enhancements:
- Ignoring expired SSL certificates to prevent fetch errors.
- Field filtering reduces payload size and focuses on key attributes.
- Proxy support with proper authentication and SSL handling.
"""

import json
import os
from typing import List, Dict
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Step 1: Get proxy details from environment
PROXY_URL = os.getenv('PROXIES')
if not PROXY_URL:
    print("Warning: No proxy configuration found in .env file")

# Parse proxy details
proxy_config = None
if PROXY_URL:
    # Extract username, password, host, and port from the proxy URL
    # Format: https://username:password@host:port
    parts = PROXY_URL.replace('https://', '').split('@')
    if len(parts) == 2:
        auth, server = parts
        auth_parts = auth.split(':')
        if len(auth_parts) >= 2:
            username = auth_parts[0]
            # Handle the case where password might contain colons
            password = ':'.join(auth_parts[1:]) if ':' in auth[len(username)+1:] else auth_parts[1]
            proxy_config = {
                "server": f"http://{server}",
                "username": username,
                "password": password
            }
            print(f"Proxy configured: {server} (authenticated)")
        else:
            print("Error parsing proxy credentials")
    else:
        print("Invalid proxy URL format")

# Step 2: List of product codes extracted from DevTools
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
OUTPUT_FILE: str = "advanced_crawler_products.json"


def fetch_all_products(codes: List[str], proxy_settings=None) -> List[Dict]:
    """
    Fetches minimal product info for each code through a simplified context.

    Args:
        codes: List of Adidas product codes.
        proxy_settings: Optional proxy configuration dictionary.
    Returns:
        Filtered list of product dictionaries with selected fields.
    """
    url_template: str = "https://www.adidas.com/plp-app/api/product/{code}?sitePath=us"
    results: List[Dict] = []

    with sync_playwright() as p:
        # Create context with proxy settings (if provided) and ignoring HTTPS errors
        context_options = {"ignore_https_errors": True}
        if proxy_settings:
            context_options["proxy"] = proxy_settings
        
        request_ctx = p.request.new_context(**context_options)

        # Add a user agent to appear more like a regular browser
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.9",
        }

        for code in codes:
            api_url = url_template.format(code=code)
            print(f"Fetching {code}...", end=" ")
            
            try:
                response = request_ctx.get(api_url, headers=headers)
                
                if response.status == 200:
                    product = response.json().get('product', {})
                    price_data = product.get('priceData', {})

                    record = {
                        'code': code,
                        'title': product.get('title'),
                        'original_price': price_data.get('price'),
                        'sale_price': price_data.get('salePrice'),
                        'on_sale': (
                            price_data.get('salePrice') is not None
                            and price_data.get('salePrice') < price_data.get('price')
                        ),
                        'in_stock': not price_data.get('isSoldOut', True),
                    }
                    results.append(record)
                    print('✔')
                else:
                    print(f'✖ HTTP {response.status}')
                    
            except Exception as e:
                print(f'✖ Error: {str(e)}')

        # Clean up request context
        request_ctx.dispose()

    return results


def main():
    # Run with proxy if configured
    if proxy_config:
        print(f"Starting fetch with proxy...")
        products = fetch_all_products(PRODUCT_CODES, proxy_config)
    else:
        print("Starting fetch without proxy...")
        products = fetch_all_products(PRODUCT_CODES)
        
    print(f"Retrieved {len(products)} product records.")

    # Write filtered results to disk
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(products, f, indent=2, ensure_ascii=False)

    print(f"✅ Written filtered results to '{OUTPUT_FILE}'")


if __name__ == '__main__':
    main()