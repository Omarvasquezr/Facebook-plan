"""Check the Italian theme schedule independently of visitor timezone.

Run with an optional served portfolio URL to also exercise manual/auto controls.
"""
import asyncio
from datetime import datetime, timezone
from pathlib import Path
import shutil
import sys

from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / 'theme-clock.js').read_text()
CASES = [
    ('2026-01-15T04:59:59Z', 'dark'),
    ('2026-01-15T05:00:00Z', 'light'),
    ('2026-01-15T16:59:59Z', 'light'),
    ('2026-01-15T17:00:00Z', 'dark'),
    ('2026-01-15T23:00:00Z', 'dark'),
    ('2026-07-15T03:59:59Z', 'dark'),
    ('2026-07-15T04:00:00Z', 'light'),
    ('2026-07-15T15:59:59Z', 'light'),
    ('2026-07-15T16:00:00Z', 'dark'),
    ('2026-03-29T00:59:59Z', 'dark'),
    ('2026-03-29T01:00:00Z', 'dark'),
    ('2026-10-25T00:59:59Z', 'dark'),
    ('2026-10-25T01:00:00Z', 'dark'),
]


async def check_portfolio(browser, base):
    context = await browser.new_context(
        timezone_id='America/Los_Angeles', color_scheme='light', reduced_motion='reduce'
    )
    page = await context.new_page()
    instant = datetime(2026, 1, 15, 16, 59, 59, 900000, tzinfo=timezone.utc)
    await page.clock.install(time=instant)
    await page.clock.pause_at(instant)
    await context.add_init_script("sessionStorage.setItem('ov-intro','1')")
    errors = []
    page.on('pageerror', lambda error: errors.append(str(error)))
    await page.goto(base, wait_until='networkidle')
    auto = page.locator('[data-theme-auto]')
    assert await page.locator('html').get_attribute('data-theme') == 'light'
    assert await auto.get_attribute('aria-pressed') == 'true'
    await page.clock.run_for(200)
    assert await page.locator('html').get_attribute('data-theme') == 'dark', 'open page missed18:00 Italy'
    await page.locator('.compact-theme').click()
    assert await page.locator('html').get_attribute('data-theme') == 'light'
    assert await auto.get_attribute('aria-pressed') == 'false'
    await page.clock.set_fixed_time(datetime(2026, 1, 15, 17, 5, tzinfo=timezone.utc))
    await page.evaluate("dispatchEvent(new Event('focus'))")
    assert await page.locator('html').get_attribute('data-theme') == 'light', 'schedule overwrote manual choice'
    await auto.click()
    assert await page.locator('html').get_attribute('data-theme') == 'dark'
    assert await auto.get_attribute('aria-pressed') == 'true'
    await page.clock.set_fixed_time(datetime(2026, 1, 16, 5, 0, tzinfo=timezone.utc))
    await page.evaluate("dispatchEvent(new Event('focus'))")
    assert await page.locator('html').get_attribute('data-theme') == 'light', '06:00 Italy not restored'
    assert not errors, errors
    await context.close()


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            executable_path=shutil.which('chromium') or shutil.which('google-chrome'),
            args=['--no-sandbox'],
        )
        for timezone_id in ['Europe/Rome', 'America/Los_Angeles', 'Asia/Tokyo']:
            context = await browser.new_context(timezone_id=timezone_id)
            page = await context.new_page()
            await page.add_script_tag(content=SOURCE)
            for instant, expected in CASES:
                actual = await page.evaluate('instant => OVThemeClock.getTheme(new Date(instant))', instant)
                assert actual == expected, (timezone_id, instant, actual, expected)
            await context.close()

        context = await browser.new_context(timezone_id='America/Los_Angeles')
        page = await context.new_page()
        instant = datetime(2026, 1, 15, 16, 59, 59, 900000, tzinfo=timezone.utc)
        await page.clock.install(time=instant)
        await page.clock.pause_at(instant)
        await page.add_script_tag(content=SOURCE)
        await page.evaluate('''() => {
          window.changes = [];
          window.stopWatching = OVThemeClock.watch(theme => changes.push(theme));
        }''')
        assert await page.evaluate('changes') == ['light']
        await page.clock.run_for(200)
        assert await page.evaluate('changes') == ['light', 'dark'], '18:00 transition missed'
        await page.clock.set_fixed_time(datetime(2026, 1, 16, 5, 0, tzinfo=timezone.utc))
        await page.evaluate("dispatchEvent(new Event('focus'))")
        assert await page.evaluate('changes') == ['light', 'dark', 'light'], 'return-to-page correction missed'
        await page.evaluate('stopWatching()')
        await page.clock.set_fixed_time(datetime(2026, 1, 16, 17, 0, tzinfo=timezone.utc))
        await page.evaluate("dispatchEvent(new Event('focus'))")
        assert await page.evaluate('changes') == ['light', 'dark', 'light'], 'watch cleanup failed'
        await context.close()

        # An unavailable timezone database must not break the page.
        context = await browser.new_context(color_scheme='dark')
        page = await context.new_page()
        await page.evaluate("() => { Intl.DateTimeFormat = function(){throw Error('unavailable timezone')}; }")
        await page.add_script_tag(content=SOURCE)
        assert await page.evaluate('OVThemeClock.getTheme()') == 'dark'
        await context.close()
        if len(sys.argv) > 1:
            await check_portfolio(browser, sys.argv[1])
        await browser.close()
    print(f'{len(CASES) * 3} schedule cases passed across three visitor timezones; live boundary, focus correction, cleanup and unavailable-Intl fallback passed.')
    if len(sys.argv) > 1:
        print('Served portfolio follows Italy time across18:00/06:00, preserves manual choice and returns to Auto on demand.')


if __name__ == '__main__':
    asyncio.run(main())
