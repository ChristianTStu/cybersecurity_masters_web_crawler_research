import requests


def crawl_version2() -> None:
    """
    Fetch page using requests and return the raw HTML content with improved handling.

    Improvements over Version 1:
    - Uses the `requests` library for simpler syntax.
    - Includes a custom User-Agent header.
    - Checks HTTP status codes and handles timeouts.
    """
    url = 'https://www.scrapethissite.com/pages/simple/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; BasicCrawler/2.0)'
    }

    try:
        # Send GET request with a 10-second timeout
        resp = requests.get(url, headers=headers, timeout=10)
        # Raise an exception for HTTP errors (4xx/5xx)
        resp.raise_for_status()

        # Print out the fetched HTML content
        print(resp.text)

    except requests.exceptions.Timeout:
        print("Error: Request timed out after 10 seconds.")
    except requests.exceptions.HTTPError as he:
        print(f"HTTP error occurred: {he}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")

if __name__ == '__main__':
    crawl_version2()
