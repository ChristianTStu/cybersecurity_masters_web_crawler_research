"""
Master's Thesis - Web Scraping Implementation: Improved Crawler - Version 2 (requests)

This script demonstrates an improved approach to web scraping using Python's
requests library, which is a popular third-party package. This version
represents a more modern implementation with better error handling and simpler syntax.

Technical overview:
- Uses requests: A high-level HTTP client library
- Automatic connection management: Handles connections efficiently
- Built-in encoding detection: Automatically converts response to text
- Simple API: Cleaner syntax compared to urllib
- Improved error handling: Specific exception types for different error scenarios
- Custom headers: Sets User-Agent for better web server interaction

Advantages of requests approach:
- Intuitive and pythonic API
- Automatic session management
- Built-in timeout handling
- Automatic content decoding
- Connection pooling for efficiency
- Comprehensive error handling capabilities
- Simpler code with fewer lines

Limitations:
- External dependency (not in standard library)
- Still no HTML parsing capability in this version
- Basic handling of response (no structured data extraction)

Target URL: https://www.scrapethissite.com/pages/simple/
This website contains information about countries which will be extracted
in different ways across the three versions of the scraper.
"""

import requests  # Popular third-party HTTP library


def crawl_version2() -> None:
    """
    Fetch page using requests and return the raw HTML content with improved handling.
    
    This function:
    1. Creates a GET request to the target website with custom headers
    2. Handles connection with automatic session management
    3. Sets a timeout to prevent hanging on slow responses
    4. Verifies successful status code with raise_for_status()
    5. Accesses the response text with automatic encoding detection
    6. Prints the entire HTML document
    
    The requests library simplifies HTTP interactions compared to urllib,
    with better error handling, connection management, and a more
    intuitive API. It's the recommended approach for most web scraping tasks.
    
    Returns:
        None: Results are printed to stdout directly
    
    Raises:
        Timeout: If the request takes longer than the specified timeout
        HTTPError: If the server returns an error status code (4xx/5xx)
        RequestException: Base class for all requests exceptions
    """
    # The target URL to be scraped
    # A simple page with country information in a structured HTML format
    url = 'https://www.scrapethissite.com/pages/simple/'
    
    # Custom headers help make the request more like a regular browser
    # This can help avoid being blocked by some websites
    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; BasicCrawler/2.0)'
    }

    try:
        # requests.get() is a high-level method that:
        # 1. Creates a connection to the server
        # 2. Sends the HTTP GET request with specified headers
        # 3. Receives and processes the HTTP response
        # 4. Returns a Response object with many helpful methods
        #
        # The timeout parameter prevents the request from hanging indefinitely
        # if the server is slow to respond
        resp = requests.get(url, headers=headers, timeout=10)
        
        # raise_for_status() checks if the response status code indicates an error
        # (4xx or 5xx) and raises an HTTPError exception if so
        # This is a more explicit way to handle HTTP errors compared to urllib
        resp.raise_for_status()

        # resp.text automatically handles the character encoding
        # The requests library determines the encoding from the HTTP headers
        # or falls back to UTF-8, saving us from manual decoding
        #
        # This is a more convenient way to access the response body
        # compared to resp.read().decode() in urllib
        print(resp.text)

    except requests.exceptions.Timeout:
        # Specific handling for timeout errors
        # This makes the error handling more informative than Version 1
        print("Error: Request timed out after 10 seconds.")
    except requests.exceptions.HTTPError as he:
        # Specific handling for HTTP status code errors (4xx/5xx)
        print(f"HTTP error occurred: {he}")
    except requests.exceptions.RequestException as e:
        # General exception for all other request errors
        # This is a catch-all for network problems, invalid URLs, etc.
        print(f"Error fetching URL: {e}")


if __name__ == '__main__':
    # This conditional ensures the main code only runs when the script is executed directly
    # and not when imported as a module into another script
    crawl_version2()