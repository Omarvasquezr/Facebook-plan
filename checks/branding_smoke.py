import asyncio,json,io,sys,shutil
from pathlib import Path
from urllib.parse import urlparse
from html.parser import HTMLParser
from PIL import Image
from playwright.async_api import async_playwright
R=Path(__file__).resolve().parents[1]
BASE=(sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:4174/dist/web/').rstrip('/')+'/'
class Head(HTMLParser):
 def __init__(self):super().__init__();self.meta={};self.links={}
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='meta':self.meta[a.get('property',a.get('name'))]=a.get('content')
  if tag=='link':self.links.setdefault(a.get('rel'),[]).append(a)
async def main():
 results=[]
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path=shutil.which('chromium') or shutil.which('google-chrome'),args=['--no-sandbox'])
  for width in [320,1440]:
   ctx=await b.new_context(viewport={'width':width,'height':900})
   page=await ctx.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
   await page.goto(BASE,wait_until='domcontentloaded')
   assert await page.locator('.brand-intro').is_visible()
   assert await page.locator('.brand-intro').get_attribute('aria-hidden')=='true'
   assert await page.locator('.brand-intro').evaluate('el=>getComputedStyle(el).pointerEvents')=='none'
   await page.wait_for_function("!document.querySelector('.brand-intro')",timeout=3000)
   await page.reload(wait_until='domcontentloaded')
   assert not await page.locator('.brand-intro').count()
   await page.goto(BASE+'?intro=1',wait_until='domcontentloaded')
   assert await page.locator('.brand-intro').is_visible()
   await page.keyboard.press('Escape')
   assert not await page.locator('.brand-intro').count()
   assert await page.locator('#language-toggle').is_visible()
   assert not errors,errors
   results.append(f'{width}px: bounded intro, once/session, replay, Escape, no JS errors')
   await ctx.close()
  ctx=await b.new_context(reduced_motion='reduce');page=await ctx.new_page()
  await page.goto(BASE+'?intro=1',wait_until='networkidle')
  assert not await page.locator('.brand-intro').count()
  results.append('Reduced motion: intro skipped')
  await ctx.close()
  ctx=await b.new_context(java_script_enabled=False);page=await ctx.new_page()
  await page.goto(BASE,wait_until='networkidle')
  assert await page.locator('.brand-intro').is_hidden()
  assert await page.locator('h1').is_visible()
  results.append('No JavaScript: content visible, intro hidden')
  await ctx.close()
  # The CSS animation must clear the overlay even if the JS cleanup cannot load.
  ctx=await b.new_context();page=await ctx.new_page()
  await page.route('**/intro.js',lambda route:route.abort())
  await page.goto(BASE+'?intro=1',wait_until='domcontentloaded')
  await page.wait_for_function("getComputedStyle(document.querySelector('.brand-intro')).visibility==='hidden'",timeout=3000)
  results.append('Intro JS unavailable: CSS hides overlay')
  await ctx.close()
  # The JS fallback must clear it if CSS is missing.
  ctx=await b.new_context();page=await ctx.new_page()
  await page.route('**/intro.css',lambda route:route.abort())
  await page.goto(BASE+'?intro=1',wait_until='domcontentloaded')
  await page.wait_for_function("!document.querySelector('.brand-intro')",timeout=3000)
  results.append('Intro CSS unavailable: bounded JS cleanup')
  await ctx.close()
  # Messaging metadata must exist in raw HTML, without running the page scripts.
  response=await b.new_context();raw=await response.request.get(BASE);head=Head();head.feed(await raw.text())
  for key in ['og:title','og:description','og:type','og:url','og:image','og:image:type','og:image:width','og:image:height','og:image:alt','twitter:card','twitter:image']:
   assert head.meta.get(key),key
  assert head.meta['twitter:card']=='summary_large_image'
  image_url=urlparse(head.meta['og:image']);assert image_url.scheme=='https' and image_url.netloc=='omar-vasquez.vercel.app'
  assert head.links['canonical'][0]['href']=='https://omar-vasquez.vercel.app/'
  for path in [image_url.path.lstrip('/'),'favicon.ico','favicon.svg','favicon-32.png','apple-touch-icon.png']:
   r=await response.request.get(BASE+path);assert r.status==200,(path,r.status)
   if path.endswith('.png'):
    image=Image.open(io.BytesIO(await r.body()))
    expected=(1200,630) if path.startswith('assets/') else (32,32) if '32' in path else (180,180)
    assert image.size==expected,(path,image.size)
    if not path.startswith('assets/'): assert image.convert('RGBA').getpixel((0,0))[3]==0,(path,'opaque icon corners')
    assert r.headers['content-type'].startswith('image/png')
   elif path.endswith('.svg'):assert 'image/svg+xml' in r.headers['content-type']
  ico=Image.open(R/'favicon.ico');assert ico.ico.sizes()=={(16,16),(32,32),(48,48)}
  assert (R/'assets/omar-vasquez-social-v1.png').stat().st_size<1_000_000
  results.append('Raw metadata, HTTPS canonical/image, MIME/dimensions, SVG/PNG/ICO icons: pass')
  await response.close();await b.close()
 print('\n'.join(results))
asyncio.run(main())
