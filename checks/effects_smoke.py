"""Check that decorative lighting settles instead of rendering continuously.

Usage: python3 checks/effects_smoke.py URL [--engine chromium|webkit|firefox]
No publishing or external requests are performed by this check.
"""
import argparse
import asyncio
import json
import shutil

from playwright.async_api import async_playwright


async def frames(page, milliseconds=1000):
    before = await page.evaluate('window.__auditAnimationFrames')
    await page.wait_for_timeout(milliseconds)
    return await page.evaluate('window.__auditAnimationFrames') - before


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    parser.add_argument('--engine', choices=['chromium', 'webkit', 'firefox'], default='chromium')
    args = parser.parse_args()
    results = []
    async with async_playwright() as p:
        engine = getattr(p, args.engine)
        launch = {}
        if args.engine == 'chromium':
            launch = {'executable_path': shutil.which('chromium') or shutil.which('google-chrome'),
                      'args': ['--no-sandbox']}
        browser = await engine.launch(**launch)
        for reduced, observer in [(False, True), (True, True), (True, False)]:
            context = await browser.new_context(
                viewport={'width': 390 if reduced else 1440, 'height': 900},
                reduced_motion='reduce' if reduced else 'no-preference',
                has_touch=reduced,
            )
            await context.add_init_script("""sessionStorage.setItem('ov-intro','1');
              localStorage.setItem('ov-theme','dark');
              window.__auditAnimationFrames=0;
              const nativeFrame=window.requestAnimationFrame.bind(window);
              window.requestAnimationFrame=callback=>nativeFrame(time=>{
                window.__auditAnimationFrames++;callback(time);
              });""")
            if not observer:
                await context.add_init_script('window.IntersectionObserver=undefined')
            page = await context.new_page()
            errors = []
            page.on('pageerror', lambda error: errors.append(str(error)))
            await page.goto(args.url, wait_until='networkidle')
            assert await page.locator('html').get_attribute('data-effects-ready') == 'true', 'effects.js was not initialized'
            await page.wait_for_timeout(1800)
            assert await frames(page) == 0, 'idle page still requests animation frames'
            if not reduced:
                await page.mouse.move(350, 200)
                # Observe convergence instead of assuming a frame rate on a
                # shared or throttled browser. A settled light must then stop.
                await page.wait_for_function("""() => {
                  const style=document.querySelector('.spot').style;
                  const x=parseFloat(style.getPropertyValue('--lx'));
                  const y=parseFloat(style.getPropertyValue('--ly'));
                  return Math.hypot(x-350,y-200)<.1;
                }""", timeout=10000)
                position = await page.locator('.spot').evaluate("""element => ({
                  x:parseFloat(element.style.getPropertyValue('--lx')),
                  y:parseFloat(element.style.getPropertyValue('--ly'))
                })""")
                assert abs(position['x'] - 350) < 1 and abs(position['y'] - 200) < 1, position
                assert await frames(page) == 0, 'pointer-follow light did not settle'
            else:
                assert await page.locator('[data-reveal].pending').count() == 0, 'reduced-motion content remains hidden'
                style = await page.locator('.spot').get_attribute('style')
                await page.touchscreen.tap(200, 300)
                await page.wait_for_timeout(200)
                assert await page.locator('.spot').get_attribute('style') == style, 'reduced-motion touch moved the light'
                assert await frames(page, 500) == 0
            assert await page.locator('.marquee > [data-marquee-copy]').count() == await page.locator('.marquee').count()
            assert await page.locator('.marquee > [data-marquee-copy]').evaluate_all(
                "elements=>elements.every(element=>element.getAttribute('aria-hidden')==='true')"
            )
            pause = page.locator('[data-marquee-pause]')
            assert await pause.count() == 1, 'language animation needs its pause control'
            await pause.scroll_into_view_if_needed()
            await pause.focus()
            assert await page.locator('.marquee').evaluate("element=>element.style.animationPlayState==='paused'"), 'focus did not pause the strip'
            await page.keyboard.press('Space')
            assert await pause.get_attribute('aria-pressed') == 'true', 'Space did not pause language animation'
            await pause.evaluate('element=>element.blur()')
            assert await page.locator('.marquee').evaluate("element=>element.style.animationPlayState==='paused'"), 'manual pause was lost after blur'
            await pause.focus()
            await page.keyboard.press('Enter')
            assert await pause.get_attribute('aria-pressed') == 'false', 'Enter did not release manual pause'
            await pause.evaluate('element=>element.blur()')
            await page.mouse.move(1, 1)
            if reduced:
                assert await page.locator('.marquee').evaluate("element=>element.style.animationPlayState==='paused'"), 'reduced motion resumed animation'
            else:
                await page.wait_for_function("document.querySelector('.marquee').style.animationPlayState!== 'paused'")
            if reduced:
                await pause.tap()
                assert await pause.get_attribute('aria-pressed') == 'true', 'touch did not toggle manual pause'
            assert not errors, errors
            results.append({'engine': args.engine, 'reduced_motion': reduced, 'intersection_observer': observer,
                            'idle_animation_frames': 0, 'passed': True})
            await context.close()
        await browser.close()
    print(json.dumps(results, indent=2))
    print('Idle rendering, finite light tracking, reduced motion, touch and missing-observer fallback passed.')


if __name__ == '__main__':
    asyncio.run(main())
