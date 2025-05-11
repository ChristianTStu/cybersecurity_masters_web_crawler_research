"""
Master's Thesis - Web Scraping Implementation: Basic Crawler - Version 1 (urllib)

This script demonstrates the most fundamental approach to web scraping using Python's
built-in urllib library, which is part of the standard library. This version
represents the baseline implementation with minimal dependencies and complexity.

Technical overview:
- Uses urllib.request: Python's built-in HTTP client from the standard library
- Direct TCP socket connection: Handles the raw HTTP request/response cycle
- Manual character decoding: Converts bytes to string with specified encoding
- No HTML parsing: Returns raw HTML content for demonstration purposes
- Basic error handling: Catches and reports exceptions without detailed handling

Advantages of urllib approach:
- No external dependencies required
- Direct control over the HTTP request lifecycle
- Low-level access to HTTP response details
- Built into Python's standard library

Limitations:
- No automatic cookie handling
- No built-in retry mechanisms
- Manual handling of redirects
- No session persistence
- No connection pooling
- Limited error handling capabilities
- More verbose code compared to higher-level libraries

Target URL: https://www.scrapethissite.com/pages/simple/
This website contains information about countries which will be extracted
in different ways across the three versions of the scraper.
"""

import urllib.request  # Python's built-in library for making HTTP requests


def crawl_version1() -> None:
    """
    Fetch page using urllib and return the raw HTML content.
    
    This function:
    1. Creates a direct HTTP request to the target website
    2. Opens a socket connection to the server
    3. Sends the HTTP GET request
    4. Receives the raw HTTP response
    5. Decodes the response bytes to string
    6. Prints the entire HTML document
    
    The urllib library handles the TCP socket connection, HTTP protocol
    formatting, and basic header management. However, unlike more advanced
    libraries, it requires manual handling of many HTTP behaviors.
    
    Returns:
        None: Results are printed to stdout directly
    
    Raises:
        URLError: If the server cannot be reached
        HTTPError: If the server returns an error status code
        ContentTooShortError: If the download is incomplete
        Other exceptions may occur during connection or parsing
    """
    # The target URL to be scraped
    # A simple page with country information in a structured HTML format
    url = 'https://www.scrapethissite.com/pages/simple/'

    try:
        # urllib.request.urlopen establishes a connection to the specified URL
        # and returns a file-like response object. The 'with' statement ensures
        # proper resource management and connection closure when done.
        #
        # Under the hood, this:
        # 1. Resolves the domain name to an IP address via DNS
        # 2. Opens a TCP socket to the server (default port 80 or 443 for HTTPS)
        # 3. Formats and sends an HTTP GET request with minimal headers
        # 4. Waits for the response headers and body to be received
        with urllib.request.urlopen(url) as resp:
            # resp.read() returns the complete response body as bytes
            # .decode('utf-8') converts the bytes to a string using UTF-8 encoding
            # 
            # Note that this loads the entire response into memory at once,
            # which could be problematic for very large pages. More advanced
            # implementations would use streaming for large responses.
            html = resp.read().decode('utf-8')
            
            # Print the raw HTML to stdout
            # This is the most basic form of handling the scraped content,
            # without any parsing or data extraction.
            # In a more advanced implementation, this HTML would be parsed
            # to extract specific information about countries.
            print(html)
            
    except Exception as e:
        # Basic error handling
        # This catches all exceptions that might occur during the HTTP request
        # or processing of the response. In production code, you would want to
        # catch more specific exceptions and handle them appropriately.
        #
        # Common errors include:
        # - urllib.error.URLError: Network problems like DNS failures or refused connections
        # - urllib.error.HTTPError: Server returned an error status code
        # - UnicodeDecodeError: Issues with character encoding
        print(f"Error fetching URL: {e}")


if __name__ == "__main__":
    # This conditional ensures the main code only runs when the script is executed directly
    # and not when imported as a module into another script
    crawl_version1()