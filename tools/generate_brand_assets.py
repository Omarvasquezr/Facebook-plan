#!/usr/bin/env python3
"""Renderiza el SVG y el diseño HTML locales. Requiere Playwright, Chromium y Pillow.

Arrancar antes un servidor de la raíz del proyecto (solo desarrollo).
Uso: python3 tools/generate_brand_assets.py http://127.0.0.1:4174/
No publica ni genera los PDF. Los PNG/ICO se conservan en Git, por lo que el
build habitual no necesita estas dependencias de diseño.
"""
import asyncio,io,shutil,sys
from pathlib import Path
from PIL import Image
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parents[1]
BASE=(sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:4174/').rstrip('/')+'/'

async def main():
    async with async_playwright() as p:
        browser=await p.chromium.launch(executable_path=shutil.which('chromium') or shutil.which('google-chrome'),args=['--no-sandbox'])
        page=await browser.new_page(viewport={'width':1200,'height':630},device_scale_factor=1)
        response=await page.goto(BASE+'tools/social-card.html',wait_until='networkidle')
        if response.status!=200:raise RuntimeError('No se puede abrir el diseño HTML')
        await page.evaluate('document.fonts.ready')
        assert await page.evaluate("document.fonts.size===3 && [...document.fonts].every(f=>f.status==='loaded')"),'Fuentes no cargadas'
        (ROOT/'assets').mkdir(exist_ok=True)
        await page.screenshot(path=str(ROOT/'assets/omar-vasquez-social-v1.png'))
        await page.set_viewport_size({'width':512,'height':512})
        response=await page.goto(BASE+'favicon.svg',wait_until='networkidle')
        if response.status!=200:raise RuntimeError('No se puede abrir el favicon SVG')
        image=Image.open(io.BytesIO(await page.screenshot(omit_background=True))).convert('RGBA')
        for size,name in [(32,'favicon-32.png'),(180,'apple-touch-icon.png')]:
            image.resize((size,size),Image.Resampling.LANCZOS).save(ROOT/name,optimize=True)
        image.save(ROOT/'favicon.ico',sizes=[(16,16),(32,32),(48,48)])
        await browser.close()
    print('Social card 1200×630, favicon SVG/ICO/PNG y Apple Touch Icon preparados.')

if __name__=='__main__':asyncio.run(main())
