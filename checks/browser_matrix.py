"""Representative browser-engine checks for the static portfolio.

This exercises real installed engines with emulated viewports/input. It does not
certify physical phones, Safari releases or Instagram's native in-app browser.
Usage: python3 checks/browser_matrix.py URL [report.json]
Optional engines use PLAYWRIGHT_BROWSERS_PATH if installed separately.
"""
import asyncio
import json
import os
from pathlib import Path
import shutil
import sys

from playwright.async_api import async_playwright

BASE = (sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:4191/').rstrip('/') + '/'
REPORT = Path(sys.argv[2]) if len(sys.argv) > 2 else None
PROFILES = [
    ('compact-phone', 320, 740, True, 2),
    ('android-standard', 360, 800, True, 3),
    ('compact-height-phone', 375, 667, True, 2),
    ('iphone-xs-size', 375, 812, True, 3),
    ('iphone-standard', 390, 844, True, 3),
    ('iphone-new-standard', 393, 852, True, 3),
    ('android-large', 412, 915, True, 3),
    ('iphone-large', 430, 932, True, 3),
    ('tablet', 768, 1024, True, 2),
    ('tablet-wide', 820, 1180, True, 2),
    ('laptop', 1366, 768, False, 1),
    ('laptop-retina-logical', 1440, 900, False, 2),
    ('desktop', 1920, 1080, False, 1),
    ('large-desktop', 2560, 1440, False, 1),
]


async def geometry(page, label):
    data = await page.evaluate('''() => {
      const rect = s => {const r=document.querySelector(s).getBoundingClientRect();
        return {left:r.left,right:r.right,top:r.top,bottom:r.bottom,width:r.width,height:r.height}};
      return {width:innerWidth,scroll:document.documentElement.scrollWidth,
              bar:rect('.bar'),name:rect('.name')};
    }''')
    assert data['scroll'] <= data['width'] + 1, (label, 'document overflow', data)
    assert data['bar']['left'] >= -1 and data['bar']['right'] <= data['width'] + 1, (label, 'bar clipped', data)
    assert data['name']['right'] <= data['width'] + 1, (label, 'name clipped', data)
    return data


async def profile_check(page, mobile, label):
    opener = page.locator('#profile-open')
    await opener.scroll_into_view_if_needed()
    if mobile:
        await opener.tap()
    else:
        await opener.click()
    dialog = page.locator('#profile-dialog')
    assert await dialog.is_visible(), (label, 'profile did not open')
    assert await dialog.evaluate("el => el.matches(':modal')"), (label, 'profile is not modal')
    portrait = dialog.locator('.profile-portrait')
    await portrait.evaluate('img => img.decode()')
    shape = await portrait.evaluate('''img => {
      const r=img.getBoundingClientRect();return {ratio:r.width/r.height,
        natural:img.naturalWidth/img.naturalHeight,fit:getComputedStyle(img).objectFit};
    }''')
    assert abs(shape['ratio'] - shape['natural']) < .005 and shape['fit'] == 'contain', (label, 'portrait cropped', shape)
    bounds = await dialog.bounding_box()
    viewport = page.viewport_size
    assert bounds and bounds['x'] >= -1 and bounds['x'] + bounds['width'] <= viewport['width'] + 1, (label, 'dialog width', bounds)
    assert bounds['y'] >= -1 and bounds['y'] + bounds['height'] <= viewport['height'] + 1, (label, 'dialog height', bounds)
    await dialog.locator('#about-omar').evaluate('el => {el.scrollTop=el.scrollHeight}')
    close = dialog.locator('[data-profile-close]')
    assert await close.evaluate('''el => {const r=el.getBoundingClientRect();return r.width>=44&&r.height>=44&&document.elementFromPoint(r.x+r.width/2,r.y+r.height/2)?.closest('[data-profile-close]')===el}'''), (label, 'close unreachable')
    await dialog.evaluate('el => {window.__matrixClosed=new Promise(done=>el.addEventListener("close",()=>done(true),{once:true}))}')
    if mobile:
        await close.tap()
    else:
        await page.keyboard.press('Escape')
    await page.evaluate('window.__matrixClosed')
    assert await dialog.is_hidden(), (label, 'profile did not close')
    assert await opener.evaluate('el=>document.activeElement===el'), (label, 'focus not returned')


async def area_check(page, mobile, label):
    for area in ['production', 'operations', 'business', 'technology']:
        button = page.locator(f'[data-area="{area}"]')
        if mobile:
            await button.tap()
        else:
            await button.click()
        panel = page.locator(f'#area-{area}')
        assert await panel.is_visible(), (label, area, 'area not visible')
        assert await page.locator('[data-area-panel]:not([hidden])').count() == 1
        disclosure = panel.locator('.area-tools-disclosure')
        assert not await disclosure.evaluate('el=>el.open'), (label, area, 'tools unexpectedly expanded')
        await disclosure.locator('summary').click()
        assert await disclosure.evaluate('el=>el.open')
        assert await disclosure.locator('.area-chip').first.is_visible()
        await disclosure.locator('summary').click()
    await page.locator('[data-area="technology"]').click()


async def run_engine(playwright, name):
    engine = getattr(playwright, name)
    kwargs = {}
    if name == 'chromium':
        executable = shutil.which('chromium') or shutil.which('google-chrome')
        if executable:
            kwargs.update(executable_path=executable, args=['--no-sandbox'])
    elif not Path(engine.executable_path).is_file():
        return {'engine':name,'available':False,'reason':'engine binary is not installed'}
    try:
        browser = await engine.launch(**kwargs)
    except Exception as error:
        return {'engine':name,'available':False,'reason':str(error).splitlines()[0]}
    result = {'engine':name,'available':True,'version':browser.version,
              'physical_devices':False,'profiles':[],'fallbacks':[]}
    try:
        for label, width, height, mobile, scale in PROFILES:
            options = {'viewport':{'width':width,'height':height},
                       'device_scale_factor':scale,'has_touch':mobile,
                       'reduced_motion':'reduce','color_scheme':'light'}
            if name != 'firefox':
                options['is_mobile'] = mobile
            context = await browser.new_context(**options)
            await context.add_init_script("sessionStorage.setItem('ov-intro','1');localStorage.setItem('ov-theme','light')")
            page = await context.new_page()
            errors=[];bad_responses=[]
            page.on('pageerror',lambda e:errors.append(str(e)))
            page.on('response',lambda response:bad_responses.append([response.status,response.url]) if response.status>=400 else None)
            await page.goto(BASE,wait_until='networkidle')
            await page.evaluate('document.fonts.ready')
            state = {'profile':label,'width':width,'height':height,'touch':mobile,'pixel_ratio':scale,'states':[]}
            for language in ['it','es','en']:
                await page.locator('#language-toggle').click()
                await page.locator(f'[data-language="{language}"]').click()
                assert await page.locator('html').get_attribute('lang') == language
                for theme in ['light','dark']:
                    if await page.locator('html').get_attribute('data-theme') != theme:
                        await page.locator('.compact-theme').click()
                    await geometry(page,(name,label,language,theme))
                    state['states'].append([language,theme])
            await profile_check(page,mobile,(name,label))
            await area_check(page,mobile,(name,label))
            assert await page.locator('a[href^="mailto:"]').count() >= 1
            assert await page.locator('a[href^="tel:"]').count() >= 1
            if not result['profiles']:
                for pdf in ['Omar-Vasquez-CV.pdf','Omar-Vasquez-CV-telefono.pdf']:
                    response = await page.request.get(BASE+pdf)
                    assert response.status == 200 and (await response.body()).startswith(b'%PDF-'),(name,label,pdf)
            # Rotation and shorter embedded-view height use the same responsive
            # page; this is emulation rather than a physical orientation test.
            if mobile:
                await page.set_viewport_size({'width':height,'height':width})
                await geometry(page,(name,label,'landscape'))
                await profile_check(page,True,(name,label,'landscape'))
            assert not errors,(name,label,errors)
            assert not bad_responses,(name,label,bad_responses)
            state['passed']=True
            result['profiles'].append(state)
            await context.close()

        # No native dialog: links must keep their inline-section fallback.
        context=await browser.new_context(viewport={'width':375,'height':667},reduced_motion='reduce')
        await context.add_init_script("sessionStorage.setItem('ov-intro','1');if(window.HTMLDialogElement)HTMLDialogElement.prototype.showModal=undefined;delete window.IntersectionObserver;")
        page=await context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
        await page.goto(BASE,wait_until='networkidle')
        assert await page.locator('#profile-dialog').count()==0
        await page.locator('#profile-open').click()
        assert await page.locator('#about-omar').is_visible()
        await page.locator('[data-area="business"]').click()
        assert await page.locator('#area-business').is_visible()
        assert not errors,('missing-capabilities',name,errors)
        result['fallbacks'].append('no native dialog / no IntersectionObserver')
        await context.close()

        context=await browser.new_context(java_script_enabled=False,viewport={'width':375,'height':667})
        page=await context.new_page();await page.goto(BASE,wait_until='networkidle')
        for area in ['production','operations','business','technology']:
            assert await page.locator(f'#area-{area}').is_visible()
        assert await page.locator('#about-omar').is_visible()
        result['fallbacks'].append('no JavaScript')
        await context.close()
    finally:
        await browser.close()
    return result


async def main():
    result={'base':BASE,'scope':'Real browser engines with emulated viewport/input; no physical phones or Instagram app tested.',
            'browser_storage':os.environ.get('PLAYWRIGHT_BROWSERS_PATH'),'engines':[]}
    async with async_playwright() as p:
        for name in ['chromium','webkit','firefox']:
            result['engines'].append(await run_engine(p,name))
    if REPORT:
        REPORT.parent.mkdir(parents=True,exist_ok=True)
        REPORT.write_text(json.dumps(result,ensure_ascii=False,indent=2))
    for engine in result['engines']:
        if engine['available']:
            print(engine['engine'],engine['version'],len(engine['profiles']),'viewport profiles;',sum(len(p['states']) for p in engine['profiles']),'theme/language states;',', '.join(engine['fallbacks']))
        else:
            print(engine['engine'],'UNAVAILABLE:',engine['reason'])


if __name__=='__main__':
    asyncio.run(main())
