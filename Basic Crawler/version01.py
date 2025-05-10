import urllib.request


def crawl_version1() -> None:
    """
    Fetch page using urllib and return the raw HTML content.
    """
    url = 'https://www.scrapethissite.com/pages/simple/'
    try:
        with urllib.request.urlopen(url) as resp:
            html = resp.read().decode('utf-8')
            # Print the raw HTML to stdout
            print(html)
    except Exception as e:
        print(f"Error fetching URL: {e}")

if __name__ == "__main__":
    crawl_version1()