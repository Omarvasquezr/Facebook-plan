import asyncio,json,sys
from pathlib import Path
from playwright.async_api import async_playwright
BASE=(sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:4174/dist/web/').rstrip('/')+'/'
async def hidden_trace(page,width,theme,step):
 try:
  await page.wait_for_function("document.documentElement.dataset.virgoVisible==='false'",timeout=5000)
 except Exception as error:
  state=await page.locator('[data-sky-trigger]').evaluate('e=>({visible:document.documentElement.dataset.virgoVisible,focused:e===document.activeElement,hovered:e.matches(":hover"),active:document.activeElement.tagName})')
  raise AssertionError((width,theme,step,state)) from error
async def close_sheet(page,method):
 # Native close queues an event after its immediate focus restoration. Wait for
 # that event before testing a new focus action, rather than racing the handler.
 await page.locator('#profile-dialog').evaluate('e=>{window.__skySheetClosed=new Promise(done=>e.addEventListener("close",()=>done(true),{once:true}))}')
 if method=='keyboard':await page.keyboard.press('Escape')
 elif method=='touch':await page.locator('#profile-dialog [data-profile-close]').tap()
 else:await page.locator('#profile-dialog [data-profile-close]').click()
 await page.evaluate('window.__skySheetClosed')
async def main():
 results=[]
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  for width,height in [(320,900),(390,844),(768,1000),(1440,1000)]:
   for theme in ['light','dark']:
    c=await b.new_context(viewport={'width':width,'height':height},color_scheme=theme,reduced_motion='reduce')
    await c.add_init_script(f"sessionStorage.setItem('ov-intro','1');localStorage.setItem('ov-language','es');localStorage.setItem('ov-theme','{theme}')")
    page=await c.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
    await page.goto(BASE,wait_until='networkidle')
    assert await page.locator('html').get_attribute('data-theme')==theme
    assert await page.get_by_role('button',name='Virgo',exact=True).count()==0
    assert await page.locator('.sky-options').count()==0
    assert (await page.locator('[data-sky-trigger]').text_content()).strip()=='Omar Vásquez'
    assert await page.locator('.sky-stars circle').count()==280
    assert await page.locator('.virgo-stars circle').count()==13
    assert await page.locator('.celestial-stage').get_attribute('aria-hidden')=='true'
    assert await page.locator('.celestial-stage').evaluate('e=>getComputedStyle(e).pointerEvents')=='none'
    assert await page.locator('.virgo-lines').evaluate('e=>getComputedStyle(e).opacity')=='0'
    assert await page.locator('.virgo-lines path').first.evaluate('e=>getComputedStyle(e).transitionDuration')=='0s'
    assert await page.evaluate('document.documentElement.scrollWidth<=innerWidth')
    # The same coordinate transformation drives the map and the CSS light source.
    sun=await page.evaluate('''() => {const s=document.querySelector('#celestial-map'),m=s.getScreenCTM(),p=new DOMPoint(+s.dataset.sunX,+s.dataset.sunY).matrixTransform(m),c=getComputedStyle(document.documentElement);return {x:p.x/innerWidth*100,y:p.y/innerHeight*100,cx:parseFloat(c.getPropertyValue('--solar-x')),cy:parseFloat(c.getPropertyValue('--solar-y'))}}''')
    assert abs(sun['x']-sun['cx'])<.001 and abs(sun['y']-sun['cy'])<.001,sun
    # Every Virgo vertex remains in the viewport, including narrow mobile screens.
    visible=await page.locator('.virgo-stars circle').evaluate_all('''es=>es.every(e=>{const p=new DOMPoint(e.cx.baseVal.value,e.cy.baseVal.value).matrixTransform(e.getScreenCTM());return p.x>=0&&p.x<=innerWidth&&p.y>=0&&p.y<=innerHeight})''')
    assert visible,(width,theme,'Virgo clipped')
    # The small signature previews the stars and opens only the personal sheet.
    btn=page.locator('[data-sky-trigger]')
    assert await page.locator('[data-sky-toggle]').count()==0
    assert await page.locator('.profile-entry,.profile-name,.name a').count()==0
    assert await btn.get_attribute('aria-pressed') is None
    await btn.scroll_into_view_if_needed()
    await page.mouse.move(1,height-1)
    await btn.focus()
    assert await page.locator('html').get_attribute('data-virgo-visible')=='true'
    await page.keyboard.press('Enter')
    assert await page.locator('#profile-dialog').is_visible()
    assert await btn.get_attribute('aria-pressed') is None
    await close_sheet(page,'keyboard')
    assert not await page.locator('#profile-dialog').is_visible()
    assert await btn.evaluate('e=>e===document.activeElement')
    await page.locator('.compact-theme').focus()
    await page.mouse.move(1,height-1)
    await hidden_trace(page,width,theme,'after keyboard dialog close')
    await page.evaluate('scrollTo(0,0)')
    assert await btn.evaluate('e=>{const r=e.getBoundingClientRect();return document.elementFromPoint(r.x+r.width/2,r.y+r.height/2)?.closest("[data-sky-trigger]")===e}'),(width,theme,'signature blocked by another layer')
    await btn.hover()
    await page.wait_for_function("document.documentElement.dataset.virgoVisible==='true'")
    await btn.click()
    assert await page.locator('#profile-dialog').is_visible()
    await close_sheet(page,'pointer')
    assert not await page.locator('#profile-dialog').is_visible()
    assert await btn.evaluate('e=>e===document.activeElement')
    await page.locator('.compact-theme').focus()
    await page.mouse.move(1,height-1)
    await hidden_trace(page,width,theme,'after pointer dialog close')
    # Mouse proximity reveals the same real segments, without a click overlay.
    await page.evaluate('scrollTo(0,0)')
    point=await page.locator('.virgo-lines path').first.evaluate('e=>{const p=e.getPointAtLength(e.getTotalLength()/2);const s=new DOMPoint(p.x,p.y).matrixTransform(e.getScreenCTM());return {x:s.x,y:s.y}}')
    await page.mouse.move(point['x'],point['y'])
    await page.wait_for_function("document.documentElement.dataset.virgoVisible==='true'")
    await page.mouse.move(1,height-1)
    await hidden_trace(page,width,theme,'after star proximity')
    assert not errors,errors
    results.append({'width':width,'theme':theme,'passed':True})
    await c.close()
  # Actual touch operation and no-JS fallback.
  c=await b.new_context(viewport={'width':390,'height':844},is_mobile=True,has_touch=True,reduced_motion='reduce');page=await c.new_page();await page.goto(BASE,wait_until='networkidle')
  btn=page.locator('[data-sky-trigger]');await btn.tap()
  assert await page.locator('#profile-dialog').is_visible()
  assert await btn.get_attribute('aria-pressed') is None
  await close_sheet(page,'touch')
  assert not await page.locator('#profile-dialog').is_visible()
  assert await btn.evaluate('e=>e===document.activeElement')
  await c.close()
  c=await b.new_context(java_script_enabled=False);page=await c.new_page();await page.goto(BASE,wait_until='networkidle');assert await page.locator('.sky-stars circle').count()==280;assert await page.locator('[data-sky-trigger]').get_attribute('href')=='#about-omar';assert await page.locator('#about-omar').is_visible();assert await page.locator('#profile-dialog').count()==0;await c.close()
  await b.close()
 print(json.dumps(results,indent=2))
 print('8 width/theme states, projection/light agreement, 13 unclipped Virgo vertices, keyboard/touch/hover, signature dialog access and focus restoration, reduced motion, no-JS and zero observed JS errors: passed.')
asyncio.run(main())
