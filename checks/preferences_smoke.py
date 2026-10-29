import asyncio,json,re,sys,shutil
from pathlib import Path
from playwright.async_api import async_playwright

ROOT=Path(__file__).resolve().parents[1]
BASE=(sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:4174/dist/web/').rstrip('/')+'/'
source=(ROOT/'preferences.js').read_text()
translations=json.loads(re.search(r'const content = (\[.*?\]);\n  const ui',source,re.S).group(1))
async def main():
 results=[]
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path=shutil.which('chromium') or shutil.which('google-chrome'),args=['--no-sandbox'])
  for width in [320,390,1440]:
   ctx=await b.new_context(viewport={'width':width,'height':900},color_scheme='light',reduced_motion='reduce')
   page=await ctx.new_page();errors=[]
   page.on('pageerror',lambda e:errors.append(str(e)))
   await page.goto(BASE,wait_until='networkidle')
   assert await page.locator('html').get_attribute('lang')=='it'
   assert await page.locator('html').get_attribute('data-theme')=='light'
   for language,index in [('it',0),('es',1),('en',2)]:
    await page.locator('#language-toggle').click()
    assert await page.locator('#language-toggle').get_attribute('aria-expanded')=='true'
    bounds=await page.locator('#language-panel').bounding_box()
    assert bounds['x']>=0 and bounds['x']+bounds['width']<=width,(width,bounds)
    await page.locator(f'[data-language="{language}"]').click()
    assert await page.locator('html').get_attribute('lang')==language
    assert await page.locator('#language-panel').is_hidden()
    assert await page.evaluate('document.activeElement.id')=='language-toggle'
    # Every content translation must be applied, including the duplicated marquees.
    texts=await page.evaluate('''() => {const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);const a=[];while(w.nextNode()){if(!w.currentNode.parentElement.closest('script,style,noscript,[data-language]'))a.push(w.currentNode.nodeValue.trim())}return a}''')
    for row in translations:
     assert row[index] in texts,(width,language,'missing translation',row[index])
     if row[index]!=row[0]: assert row[0] not in texts,(width,language,'Italian leak',row[0])
    for theme in ['light','dark']:
     if await page.locator('html').get_attribute('data-theme')!=theme:
      await page.locator('.compact-theme').click()
     assert await page.locator('[data-theme-toggle]').evaluate_all('(buttons)=>buttons.every(b=>b.getAttribute("aria-checked")===String(document.documentElement.dataset.theme==="dark"))')
     assert await page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(width,language,theme,'overflow')
     assert await page.locator('.name').evaluate('el=>el.getBoundingClientRect().right<=innerWidth'),(width,'name')
     results.append({'width':width,'language':language,'theme':theme,'passed':True})
   # Footer controls the same preference; persistence is verified after reload.
   await page.locator('.theme-switch').click()
   target=await page.locator('html').get_attribute('data-theme')
   await page.reload(wait_until='networkidle')
   assert await page.locator('html').get_attribute('lang')=='en'
   assert await page.locator('html').get_attribute('data-theme')==target
   # Keyboard opening, selection and Escape dismissal.
   await page.locator('#language-toggle').focus()
   await page.keyboard.press('Enter')
   await page.keyboard.press('Home')
   await page.keyboard.press('ArrowDown')
   assert await page.evaluate('document.activeElement.dataset.language')=='es'
   await page.keyboard.press('Enter')
   assert await page.locator('html').get_attribute('lang')=='es'
   await page.keyboard.press('Enter')
   await page.keyboard.press('Escape')
   assert await page.locator('#language-panel').is_hidden()
   assert await page.evaluate('document.activeElement.id')=='language-toggle'
   for name in ['Omar-Vasquez-CV.pdf','Omar-Vasquez-CV-telefono.pdf','preferences.js','preferences.css']:
    r=await page.request.get(BASE+name)
    assert r.status==200,(name,r.status)
   assert not errors,errors
   await ctx.close()
  # System preference: default follows it, manual choice overrides later changes.
  ctx=await b.new_context(color_scheme='dark',reduced_motion='reduce')
  page=await ctx.new_page();await page.goto(BASE,wait_until='networkidle')
  assert await page.locator('html').get_attribute('data-theme')=='dark'
  await page.emulate_media(color_scheme='light')
  await page.wait_for_function("document.documentElement.dataset.theme==='light'")
  assert await page.locator('html').get_attribute('data-theme')=='light'
  await page.locator('.compact-theme').click()
  await page.emulate_media(color_scheme='dark');await page.emulate_media(color_scheme='light')
  await page.wait_for_timeout(100)
  assert await page.locator('html').get_attribute('data-theme')=='dark'
  # Storage unavailable must not disable translation or switches.
  await ctx.close()
  ctx=await b.new_context(reduced_motion='reduce')
  await ctx.add_init_script("Storage.prototype.getItem=function(){throw Error('blocked')};Storage.prototype.setItem=function(){throw Error('blocked')}")
  page=await ctx.new_page();await page.goto(BASE,wait_until='networkidle')
  await page.locator('#language-toggle').click();await page.locator('[data-language="en"]').click()
  assert await page.locator('html').get_attribute('lang')=='en'
  await page.locator('.theme-switch').click()
  assert await page.locator('html').get_attribute('data-theme')=='dark'
  await ctx.close();await b.close()
 print(json.dumps({'combinations':results},indent=2))
 print(f'{len(results)} combinations passed; keyboard, persistence, system preference, blocked storage and assets passed.')
asyncio.run(main())
