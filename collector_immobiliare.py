import asyncio
import json
import re
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async_api
import time
import random

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-accelerated-2d-canvas',
                '--no-first-run',
                '--no-zygote',
                '--disable-gpu',
                '--disable-blink-features=AutomationControlled',
                '--disable-web-security',
                '--disable-features=VizDisplayCompositor',
                '--disable-extensions',
                '--disable-plugins',
                '--disable-default-apps',
                '--disable-background-timer-throttling',
                '--disable-backgrounding-occluded-windows',
                '--disable-renderer-backgrounding',
                '--disable-field-trial-config',
                '--disable-back-forward-cache',
                '--disable-hang-monitor',
                '--disable-ipc-flooding-protection',
                '--disable-popup-blocking',
                '--disable-prompt-on-repost',
                '--force-fieldtrials=*BackgroundTabOpening/*Disabled/',
                '--disable-component-extensions-with-background-pages'
            ]
        )
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            viewport={'width': 1280, 'height': 720},
            locale='it-IT',
            timezone_id='Europe/Rome',
            geolocation={'latitude': 41.9028, 'longitude': 12.4964},
            permissions=['geolocation']
        )
        page = await context.new_page()
        await stealth_async_api(page)
        await page.goto("https://www.immobiliare.it/", wait_until='domcontentloaded')

        # Simulate human behavior
        await page.wait_for_timeout(random.randint(2000, 5000))
        await page.mouse.move(random.randint(100, 500), random.randint(100, 500))
        await page.wait_for_timeout(random.randint(1000, 3000))

        # Search for apartments in Rome
        await page.fill('input[name="q"]', 'roma')
        await page.wait_for_timeout(random.randint(500, 1500))
        await page.click('button[type="submit"]')
        await page.wait_for_load_state('networkidle')

        # Simulate scrolling
        await page.wait_for_timeout(random.randint(2000, 4000))
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight / 2)")
        await page.wait_for_timeout(random.randint(1000, 2000))
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await page.wait_for_timeout(random.randint(2000, 4000))

        # Extract data
        listings = await page.query_selector_all('.listing-item')
        data = []
        for listing in listings:
            title_elem = await listing.query_selector('.listing-item_title')
            price_elem = await listing.query_selector('.listing-item_price')
            if title_elem and price_elem:
                title = await title_elem.inner_text()
                price = await price_elem.inner_text()
                data.append({
                    'title': title.strip(),
                    'price': price.strip()
                })

        print(json.dumps(data, indent=4))
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
