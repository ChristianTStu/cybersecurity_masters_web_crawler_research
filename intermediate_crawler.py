import httpx
from selectolax.parser import HTMLParser

url = "https://www.rei.com/c/backpacking-packs"

headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"}

resp = httpx.get(url, headers=headers, timeout=30.0)
print(resp.status_code)
