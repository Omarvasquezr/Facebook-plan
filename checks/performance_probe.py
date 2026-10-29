"""Read local resource use before and after opening the personal portrait.

This is a resource/regression probe, not a field Core Web Vitals measurement.
Usage: python3 checks/performance_probe.py URL [--report /path/report.json]
"""
import argparse
import asyncio
import json
from pathlib import Path
import shutil
from urllib.parse import urlsplit

from playwright.async_api import async_playwright


async def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('url')
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    base = args.url.rstrip('/') + '/'
    origin = urlsplit(base)
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(
            executable_path=shutil.which('chromium') or shutil.which('google-chrome'),
            args=['--no-sandbox'],
        )
        context = await browser.new_context(viewport={'width': 390, 'height': 844}, is_mobile=True, has_touch=True, device_scale_factor=3)
        page = await context.new_page()
        requests = []
        errors = []
        page.on('request', lambda request: requests.append(request.url))
        page.on('pageerror', lambda error: errors.append(str(error)))
        await page.goto(base, wait_until='networkidle')
        await page.evaluate('document.fonts.ready')
        # Resource entries expose encoded/decoded bodies and transport overhead.
        initial = await page.evaluate('''() => performance.getEntriesByType('resource').map(entry => ({
          url:entry.name, initiator:entry.initiatorType, transferBytes:entry.transferSize,
          encodedBodyBytes:entry.encodedBodySize, decodedBodyBytes:entry.decodedBodySize
        }))''')
        initial_requests = list(requests)
        portrait_url = await page.locator('.profile-portrait').get_attribute('src')
        assert portrait_url, 'Missing portrait source'
        assert not any('omar-vasquez-portrait' in url for url in initial_requests), 'Portrait downloaded before personal sheet was opened'
        assert not any(urlsplit(url).path.lower().endswith('.pdf') for url in initial_requests), 'PDF downloaded without a request from the visitor'
        assert not any('omar-vasquez-social' in url for url in initial_requests), 'Social card loaded as a page resource'
        assert all(urlsplit(url).netloc == origin.netloc for url in initial_requests), initial_requests
        preloads = await page.locator('link[rel="preload"][as="font"]').evaluate_all('elements => elements.map(element => element.href)')
        assert len(preloads) == 2
        for url in preloads:
            assert initial_requests.count(url) == 1, (url, 'Missing or duplicate critical font request')
        await page.locator('#profile-open').tap()
        portrait = page.locator('.profile-portrait')
        await portrait.evaluate('image => image.decode()')
        assert await portrait.evaluate('image => image.complete && image.naturalWidth > 0')
        await page.wait_for_load_state('networkidle')
        after = await page.evaluate('''() => performance.getEntriesByType('resource').filter(entry => entry.name.includes('omar-vasquez-portrait')).map(entry => ({
          url:entry.name, transferBytes:entry.transferSize,
          encodedBodyBytes:entry.encodedBodySize, decodedBodyBytes:entry.decodedBodySize
        }))''')
        assert len(after) == 1, ('Portrait did not load exactly once', after)
        assert all(urlsplit(url).netloc == origin.netloc for url in requests), requests
        assert not errors, errors
        navigation = await page.evaluate('''() => {
          const entry=performance.getEntriesByType('navigation')[0];
          return {transferBytes:entry.transferSize,encodedBodyBytes:entry.encodedBodySize,decodedBodyBytes:entry.decodedBodySize};
        }''')
        report = {
            'scope': 'Chromium mobile-size resource probe against a local static HTTP server; not Instagram/Safari hardware or field CWV',
            'origin': base,
            'browser': browser.version,
            'viewport': {'width':390,'height':844,'deviceScaleFactor':3,'touch':True},
            'navigation': navigation,
            'initial': {
                'requests': len(initial_requests),
                'resourceEncodedBodyBytes': sum(entry['encodedBodyBytes'] for entry in initial),
                'resourceTransferBytes': sum(entry['transferBytes'] for entry in initial),
                'totalEncodedBodyBytes': navigation['encodedBodyBytes'] + sum(entry['encodedBodyBytes'] for entry in initial),
                'criticalFontPreloads': preloads,
                'portraitRequested': False,
                'pdfRequested': False,
                'externalRequests': [],
                'resources': initial,
            },
            'portraitAfterOpening': after,
            'observedJavaScriptErrors': errors,
        }
        if args.report:
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
        print(json.dumps({key:value for key,value in report.items() if key != 'initial'}, ensure_ascii=False, indent=2))
        print(f"Initial encoded body total: {report['initial']['totalEncodedBodyBytes']} bytes; portrait loads only when opened; fonts once; no PDF/social/external request or JS error.")
        await context.close()
        await browser.close()


if __name__ == '__main__':
    asyncio.run(main())
