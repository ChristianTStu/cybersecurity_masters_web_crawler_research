"""
Version 2: Playwright + Stealth + Proxy + CF + Cookie + Debug
---------------------------------------------------------------
PURPOSE:
  • Show that we’ve bypassed the 403 forbidden from Version 1  
  • Hit Napaonline through your rotating residential proxy  
  • Perform CF clearance, inject store cookie  
  • Dump screenshot + raw HTML → still no product cards in the DOM  

USAGE:
  1) pip install playwright playwright-stealth python-dotenv  
  2) playwright install  
  3) In `.env`, set:
       PROXIES=http://<user>:<pass>@us.decodo.com:10000
       STORE_COOKIE_NAME=napa-store
       STORE_COOKIE_VALUE=MjY4NzU=
     (ensure `.env` is gitignored)  
  4) Run:
       python version02_debug.py
"""

import os, asyncio, re, urllib.parse
from dotenv import load_dotenv
from playwright.async_api import async_playwright, Page
from playwright_stealth import stealth_async

# ─── Load & validate .env ───────────────────────────────────────────────────────
load_dotenv()
raw_proxy = os.getenv("PROXIES", "").strip()
STORE_COOKIE_NAME  = os.getenv("STORE_COOKIE_NAME")
STORE_COOKIE_VALUE = os.getenv("STORE_COOKIE_VALUE")
if not raw_proxy or not STORE_COOKIE_NAME or not STORE_COOKIE_VALUE:
    raise RuntimeError("Please set PROXIES, STORE_COOKIE_NAME & STORE_COOKIE_VALUE in .env")

# ─── Parse proxy URL ─────────────────────────────────────────────────────────────
p = urllib.parse.urlparse(raw_proxy)
proxy_cfg = {
    "server":   f"{p.scheme}://{p.hostname}:{p.port}",
    "username": urllib.parse.unquote(p.username),
    "password": urllib.parse.unquote(p.password),
}

# ─── URLs & selectors ────────────────────────────────────────────────────────────
HOMEPAGE_URL  = "https://www.napaonline.com"
CATEGORY_URL  = (
    "https://www.napaonline.com/en/shop/"
    "replacement-parts/batteries/automotive-batteries/car-batteries/315705233"
)
CONTAINER_SEL = "geo-product-list-item"
TITLE_SEL     = "div.geo-pod-detail"
PRICE_SEL     = "div.geo-plp-product_base_price"

# ─── Browser emulation ──────────────────────────────────────────────────────────
USER_AGENT  = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/135.0.0.0 Safari/537.36"
)
LOCALE       = "en-US"
TIMEZONE_ID  = "America/Chicago"

# ─── Instrumentation helper ─────────────────────────────────────────────────────
async def instrument(page: Page):
    page.on("request",  lambda req: print(f"→ REQUEST {req.method} {req.url}"))
    page.on("response", lambda res: print(f"← RESPONSE {res.status} {res.url}"))
    page.on("console",   lambda msg: print(f"[PAGE LOG] {msg.type}: {msg.text}"))
    page.on("pageerror", lambda exc: print(f"[PAGE ERROR] {exc}"))

async def run_debug():
    print("🔑 Proxy config:", proxy_cfg)
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            proxy=proxy_cfg,
            user_agent=USER_AGENT,
            locale=LOCALE,
            timezone_id=TIMEZONE_ID,
        )
        page = await context.new_page()
        await stealth_async(page)
        await instrument(page)

        # Cloudflare clearance
        print("⏳ Visiting homepage…")
        await page.goto(HOMEPAGE_URL, wait_until="networkidle")
        await page.wait_for_timeout(2000)

        # Inject store cookie
        print(f"🍪 Injecting cookie: {STORE_COOKIE_NAME}={STORE_COOKIE_VALUE}")
        await context.add_cookies([{
            "name":     STORE_COOKIE_NAME,
            "value":    STORE_COOKIE_VALUE,
            "domain":   ".napaonline.com",
            "path":     "/",
            "httpOnly": False,
            "secure":   True,
            "sameSite": "Lax"
        }])

        # Navigate to category
        print("⏳ Navigating to category…")
        await page.goto(CATEGORY_URL, wait_until="networkidle")

        # Dump screenshot + HTML
        await page.screenshot(path="debug_after_goto.png")
        print("💾 Saved debug_after_goto.png")

        # Try to scrape (will be zero)
        try:
            await page.wait_for_selector(CONTAINER_SEL, timeout=10_000)
        except:
            print("⚠️ Product grid never appeared.")
        count = await page.locator(CONTAINER_SEL).count()
        print(f"🔍 Detected {count} product cards")

        await context.close()
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run_debug())
