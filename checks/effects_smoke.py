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


async def language_sample(page):
    return await page.locator('.marquee-langs').evaluate("""async element => {
      const animation=element.getAnimations().find(item=>item.animationName==='marquee');
      await animation.ready;
      return {time:Number(animation.currentTime),timeline:document.timeline.currentTime,
              rate:animation.playbackRate,duration:animation.effect.getTiming().duration,
              x:new DOMMatrixReadOnly(getComputedStyle(element).transform).m41};
    }""")


async def check_language_motion(page):
    strip = page.locator('.language-strip')
    await strip.scroll_into_view_if_needed()
    await page.mouse.move(1, 1)
    await page.wait_for_function("getComputedStyle(document.querySelector('.marquee-langs')).animationPlayState==='running'")
    normal = await language_sample(page)
    await page.wait_for_timeout(350)
    moving = await language_sample(page)
    assert normal['rate'] == moving['rate'] == 1
    assert .8 < (moving['time']-normal['time'])/(moving['timeline']-normal['timeline']) < 1.2
    await strip.hover()
    slow = await language_sample(page)
    assert slow['rate'] == .06, slow
    assert slow['duration'] == normal['duration'] == 22000, 'speed change restarted the CSS cycle'
    assert moving['time']-30 <= slow['time'] <= moving['time']+slow['timeline']-moving['timeline']+30, 'hover jumped the timeline'
    await page.wait_for_timeout(600)
    slowed = await language_sample(page)
    observed_rate = (slowed['time']-slow['time'])/(slowed['timeline']-slow['timeline'])
    assert .035 < observed_rate < .09, ('hover must keep moving very slowly', observed_rate)
    assert abs(slowed['x']-slow['x']) > .05, 'hover froze the text'
    await page.mouse.move(1, 1)
    resumed = await language_sample(page)
    assert resumed['rate'] == 1
    assert slowed['time']-30 <= resumed['time'] <= slowed['time']+resumed['timeline']-slowed['timeline']+30, 'pointer leave jumped the timeline'
    # Offscreen suspension must not consume a JS rendering loop.
    await page.locator('h1').scroll_into_view_if_needed()
    await page.wait_for_function("getComputedStyle(document.querySelector('.marquee-langs')).animationPlayState==='paused'")
    await page.wait_for_function("""() => {
      const style=document.querySelector('.spot').style;
      return Math.hypot(parseFloat(style.getPropertyValue('--lx'))-1,
                        parseFloat(style.getPropertyValue('--ly'))-1)<.1;
    }""", timeout=10000)
    await page.wait_for_timeout(250)
    assert await frames(page) == 0
    return {'normal_rate':1, 'hover_rate':slow['rate'], 'measured_hover_rate':round(observed_rate,3), 'continuous':True}


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
        for reduced, observer in [(False, True), (False, False), (True, True), (True, False)]:
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
            assert await page.locator('[data-marquee-pause]').count() == 0
            assert await page.locator('.marquee-langs > .seq-langs:not([data-marquee-copy]) .lang').count() == 3
            assert await page.locator('.marquee-langs > [data-marquee-copy]').get_attribute('aria-hidden') == 'true'
            motion_result = None
            if reduced:
                assert await page.locator('.marquee-langs').evaluate("element=>getComputedStyle(element).animationName") == 'none'
                assert await page.locator('[data-marquee-copy]').is_hidden()
            elif observer:
                motion_result = await check_language_motion(page)
            else:
                await page.locator('.language-strip').scroll_into_view_if_needed()
                await page.mouse.move(1, 1)
                await page.wait_for_function("getComputedStyle(document.querySelector('.marquee-langs')).animationPlayState==='running'")
                assert (await language_sample(page))['rate'] == 1
            assert not errors, errors
            results.append({'engine': args.engine, 'browser_version':browser.version, 'reduced_motion': reduced, 'intersection_observer': observer,
                            'idle_animation_frames': 0, 'language_motion':motion_result, 'passed': True})
            await context.close()
        for fallback in ('no-web-animations', 'no-js'):
            context = await browser.new_context(viewport={'width':320,'height':740}, java_script_enabled=fallback!='no-js')
            if fallback == 'no-web-animations':
                await context.add_init_script("Element.prototype.getAnimations=undefined;sessionStorage.setItem('ov-intro','1')")
            page = await context.new_page()
            await page.goto(args.url, wait_until='networkidle')
            await page.evaluate('document.fonts.ready')
            assert await page.locator('[data-marquee-pause]').count() == 0
            assert await page.locator('.marquee-langs .lang').count() == 3
            assert await page.locator('.marquee-langs').evaluate("element=>getComputedStyle(element).animationName") == 'none'
            assert await page.locator('.marquee-langs .lang').evaluate_all("""elements=>elements.every(element=>{
              const rect=element.getBoundingClientRect();
              return rect.width>0 && rect.left>=0 && rect.right<=innerWidth;
            })"""), 'static languages clipped in fallback'
            results.append({'engine':args.engine,'browser_version':browser.version,'fallback':fallback,'passed':True})
            await context.close()
        await browser.close()
    print(json.dumps(results, indent=2))
    print('Idle rendering, finite light tracking, reduced motion, touch and missing-observer fallback passed.')


if __name__ == '__main__':
    asyncio.run(main())
